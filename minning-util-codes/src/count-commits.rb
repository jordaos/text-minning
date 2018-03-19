#!/usr/bin/env ruby

require 'git'
require 'sqlite3'

help_and_quit if ARGV.size < 1
ALLREPOPATHS = ARGV

def main
  ALLREPOPATHS.each do |repo_path|
    project = File.basename(repo_path).gsub('__', '/')
    i = 0
    commit_log(repo_path) do |commit|
      i+=1
    end
    puts i
  end
end

def help_and_quit
  puts 'params: DBPATH, REPOPATH'
  exit 0
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