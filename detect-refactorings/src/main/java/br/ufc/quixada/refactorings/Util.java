package br.ufc.quixada.refactorings;

import java.io.File;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class Util {
	int qtdDirs(String dirPath) {
		File f = new File(dirPath);
	    File[] files = f.listFiles();

	    int count = 0;
	    if (files != null)
	    for (int i = 0; i < files.length; i++) {
	        File file = files[i];
	        if (file.isDirectory()) {   
	        	count++;
	        }
	    }
    	return count;
    }
	
	public Connection connect(String parts_path, int part) {
        // SQLite connection string
        String url = "jdbc:sqlite:" + parts_path + "/" + part + "_part/" + part + "_part.sqlite";
        Connection conn = null;
        try {
            conn = DriverManager.getConnection(url);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
        return conn;
    }
	
	public List<String> getCommitList(String parts_path, int part) throws SQLException {
		List<String> listCommits = new ArrayList<String>();
		String sql = "SELECT * FROM commits";
		Connection conn = this.connect(parts_path, part);
		Statement stmt = (Statement) conn.createStatement();
		ResultSet rs = stmt.executeQuery(sql);
		
		while (rs.next()) {
			listCommits.add(rs.getString("sha"));
        }
		
		return listCommits;
	}
	
	private boolean fileExists(String path) {
		File f = new File(path);
		if(f.exists() && !f.isDirectory()) { 
		    return true;
		}
		return false;
	}
	
	public String getClassification(String part_path, String sha) {
		String classif_path = part_path + "/txt_ss";
		if(fileExists(classif_path + "/pos/" + sha + ".txt"))
			return "pos";
		else if (fileExists(classif_path + "/neg/" + sha + ".txt")) 
			return "neg";
		else if (fileExists(classif_path + "/neu/" + sha + ".txt"))
			return "neu";
		return "none";
	}
}
