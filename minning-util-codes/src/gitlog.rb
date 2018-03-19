#!/usr/bin/env ruby

require 'git'
require 'sqlite3'

help_and_quit if ARGV.size < 2
DBPATH = ARGV.shift
ALLREPOPATHS = ARGV

def main
  ALLREPOPATHS.each do |repo_path|
    project = File.basename(repo_path).gsub('__', '/')
    puts "Extracting log from #{project}"
    db = init_database(DBPATH)
    commit_log(repo_path) do |commit|
      insert_commit(db, commit, project)
    end
  end
end

def help_and_quit
  puts 'params: DBPATH, REPOPATH'
  exit 0
end

def insert_commit(db, commit, project)
  sql = <<-SQL
    INSERT INTO commits (
      project,
      sha,
      message,
      date,
      author_name,
      author_email)
    VALUES (?, ?, ?, ?, ?, ?)
  SQL
  db.execute(sql, [
    project, commit.sha, commit.message, commit.date.to_s,
    commit.author.name, commit.author.email])
end

def init_database(db_path)
  db = SQLite3::Database.new(db_path)
  db.execute <<-SQL
  create table if not exists commits (
    project varchar,
    sha varchar,
    message varchar,
    date varchar,
    author_name varchar,
    author_email varchar,
    UNIQUE (project, sha) ON CONFLICT REPLACE
  );
  SQL
  db
end

def commit_log(repo_path)
  begin
    g = Git.open(repo_path)
    g.log(nil).each do |commit|
      yield commit
    end
  rescue => e
    puts e.message
    puts e.backtrace.inspect
  end
end

main