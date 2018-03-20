package br.ufc.quixada.refactorings;

import java.sql.Statement;
import java.io.File;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.revwalk.RevCommit;

import refdiff.core.RefDiff;
import refdiff.core.api.GitService;
import refdiff.core.rm2.model.refactoring.SDRefactoring;
import refdiff.core.util.GitServiceImpl;

/**
 * Hello world!
 *
 */
public class App 
{
	public static void main( String[] args )
	{
		// ONLY NEED TO CHANGE THIS:
		String PROJECT = "RxJava";

		// Settings
		String PATH = "./../minning-util-codes/DBs/" + PROJECT;
		String REPO_PATH = "./../minning-util-codes/projects/" + PROJECT;
		String PARTS_PATH = PATH + "/parts";
		RefDiff refDiff = new RefDiff();
		GitService gitService = new GitServiceImpl();
		Util util = new Util();

		int qtdDirs = util.qtdDirs(PARTS_PATH);
		try {
			PrintWriter pw = new PrintWriter(new File(PATH + "/" + PROJECT + "-refactorings.csv"));
			StringBuilder sb = new StringBuilder();
			sb.append("part");
			sb.append(',');
			sb.append("Commits neg com refator");
			sb.append(',');
			sb.append("Commits neu com refator");
			sb.append(',');
			sb.append("Commits pos com refator");
			sb.append('\n');
			
			for (int i = 1; i <= qtdDirs; i++) {

				int qtdPos = 0;
				int qtdNeg = 0;
				int qtdNeu = 0;
				int qtdCommitsComRefat = 0;

				// Carregando o repositório localmete
				Repository repository = gitService.cloneIfNotExists(REPO_PATH + "_parts/interval_" + i, "");

				// Pegando a lista de commits
				List<String> commits = util.getCommitList(PARTS_PATH, i);
				System.out.println("Parte " + i + " tem " + commits.size() + " commits.");
				for(int j = 0; j < commits.size(); j++) {
					String sha = commits.get(j);
					List<SDRefactoring> refactorings = new ArrayList<SDRefactoring>();
					refactorings = refDiff.detectAtCommit(repository, sha);
					if(refactorings.size() > 0) {
						qtdCommitsComRefat++;
						String classification = util.getClassification(PARTS_PATH + "/" + i + "_part", sha);
						if (classification.toLowerCase().indexOf(("none").toLowerCase()) == -1) {
							System.out.println(classification);
							if (classification.toLowerCase().indexOf(("pos").toLowerCase()) != -1) 
								qtdPos++;
							else if(classification.toLowerCase().indexOf(("neg").toLowerCase()) != -1) 
								qtdNeg++;
							else if(classification.toLowerCase().indexOf(("neu").toLowerCase()) != -1) 
								qtdNeu++;
						}
					}
				}
				sb.append("part_" + i);
				sb.append(',');
				sb.append(qtdNeg);
				sb.append(',');
				sb.append(qtdNeu);
				sb.append(',');
				sb.append(qtdPos);
				sb.append('\n');

				System.out.println("-- " + qtdCommitsComRefat + " commits com refatorações.");
			}
			pw.write(sb.toString());
			pw.close();
		}catch (SQLException e) {
			System.out.println(e.getMessage());
		}catch (Exception e) {
			System.err.println(e.getMessage());
		}

	}
}