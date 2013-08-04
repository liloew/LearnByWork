import java.sql.CallableStatement;
import java.sql.DriverManager;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Types;

import java.sql.PreparedStatement;
import java.sql.ResultSet;

import java.util.Random;
import java.util.concurrent.BlockingQueue;

public class callProcedure implements Runnable {

    initPool inPool = new initPool();
    
	public callProcedure(initPool in) {
		// Initialize by initPool()
    	this.inPool = in;
    }
	
	public callProcedure(BlockingQueue<String> pool) {
		// Initialize by executeQuery()
		executeQuery(pool);
	}

	public Connection createConnect() {
        try {
            Class.forName("oracle.jdbc.driver.OracleDriver");
        } catch (ClassNotFoundException e) {
            System.out.println("JDBC not found");
            e.printStackTrace();
            return null;
        }
        
        Connection conn = null;
        
        try {
            conn = DriverManager.getConnection(
                    "jdbc:oracle:thin:@IP:Port:SID",
                    "username",
                    "password");
        } catch (SQLException e) {
            System.out.println("Connection error.");
            e.printStackTrace();
            return null;
        }
		
		return conn;
	}
		
       public void executeSQL(int id,String name,long longId) {
		Connection conn = createConnect();
		try {
			String sql = "INSERT INTO t(ID,NAME,LONG_ID) VALUES(?,?,?)";
			PreparedStatement pstmt = conn.prepareStatement(sql);
			pstmt.setInt(1,id);
			pstmt.setString(2, name);
			pstmt.setLong(3, longId);
			pstmt.executeUpdate();
		} catch (SQLException e) {
			System.out.println("Execute SQL Error.");
			e.printStackTrace();
		}
	}
	
	public void executeQuery(BlockingQueue<String> pool) {
		Connection conn = createConnect();
		try {
			//String sql = "select ykth from dscai_xh";
			//String sql = "SELECT NAME FROM T2";
			String sql = "select xh from T_XJ_JBXX where rownum < 100";
			PreparedStatement pstmt = conn.prepareStatement(sql);
			ResultSet rs = pstmt.executeQuery();
					
			while (rs.next()) {
				pool.add(rs.getString("xh"));
			}
		} catch (SQLException e) {
			System.out.println("Execute Query Error.");
		}
	}
	
	public void executePro(int ykth) {
		Connection conn = createConnect();
		String sql = "call p_xjgl_xjsh_JDJS_grdscai(3,2012,?,?,?)";
		try {
			String resul = "";
			CallableStatement cs = conn.prepareCall(sql);
			cs.setInt(1, ykth);
			cs.setString(2, "system");
			cs.registerOutParameter(3, java.sql.Types.VARCHAR);
			
			cs.executeUpdate();
			resul = cs.getString(3);
			if (!resul.equals("1")) {
				// TODO Log into the log ?
				System.out.println(resul);
				System.out.println(ykth + " dosent execute! ");
			}
			//System.out.println("Execute result is: " + resul + " " + ykth);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
    
    public void run() {
        Random rand = new Random();
        long threadId = Thread.currentThread().getId();
        String ykth = null;
        while(true) {
        	if (inPool.pool.isEmpty())
        		break;
        	//name = inPool.deQueue();
        	ykth = inPool.deQueue();
			//executeSQL(rand.nextInt(), name, threadId);
        	executePro( Integer.parseInt(ykth));
            System.out.println("Thread " + threadId + " has been executed: " + ykth);
        }
    }
}
