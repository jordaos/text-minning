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
			sb.append("Commits NEG com refator");
			sb.append(',');
			sb.append("Total refatorações em NEG");
			sb.append(',');
			sb.append("Commits NEU com refator");
			sb.append(',');
			sb.append("Total refatorações em NEU");
			sb.append(',');
			sb.append("Commits POS com refator");
			sb.append(',');
			sb.append("Total refatorações em POS");
			sb.append('\n');
			
			for (int i = 1; i <= qtdDirs; i++) {
				int qtdNeg = 0;
				int qtdNegRef = 0; // Quantidade de refatorações nos commits negativos para essa parte
				int qtdPos = 0;
				int qtdPosRef = 0; // Quantidade de refatorações nos commits positivos para essa parte
				int qtdNeu = 0;
				int qtdNeuRef = 0; // Quantidade de refatorações nos commits neutros para essa parte
				int qtdCommitsComRefat = 0;

				// Carregando o repositório localmete
				Repository repository = gitService.cloneIfNotExists(REPO_PATH, "");

				// Pegando a lista de commits
				List<String> commits = util.getCommitList(PARTS_PATH, i);
				System.out.println("Parte " + i + " tem " + commits.size() + " commits.");
				for(int j = 0; j < commits.size(); j++) {
					String sha = commits.get(j);
					List<SDRefactoring> refactorings = new ArrayList<SDRefactoring>();
					refactorings = refDiff.detectAtCommit(repository, sha);
					int qtdRefatoracoes = refactorings.size();
					if(qtdRefatoracoes > 0) {
						qtdCommitsComRefat++;
						String classification = util.getClassification(PARTS_PATH + "/" + i + "_part", sha);
						if (classification.toLowerCase().indexOf(("none").toLowerCase()) == -1) {
							if (classification.toLowerCase().indexOf(("pos").toLowerCase()) != -1) {
								qtdPos++;
								qtdPosRef += qtdRefatoracoes;
							}else if(classification.toLowerCase().indexOf(("neg").toLowerCase()) != -1) {
								qtdNeg++;
								qtdNegRef += qtdRefatoracoes;
							}else if(classification.toLowerCase().indexOf(("neu").toLowerCase()) != -1) {
								qtdNeu++;
								qtdNeuRef += qtdRefatoracoes;
							}
						}
					}
				}
				sb.append("part_" + i);
				sb.append(',');
				sb.append(qtdNeg);
				sb.append(',');
				sb.append(qtdNegRef);
				sb.append(',');
				sb.append(qtdNeu);
				sb.append(',');
				sb.append(qtdNeuRef);
				sb.append(',');
				sb.append(qtdPos);
				sb.append(',');
				sb.append(qtdPosRef);
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