import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.*;

/*http://localhost:8087/ptsb_war_exploded/runpg?p_gnd=Man&p_dt=16-12-1969&p_rgn=44&p_prf=40500*/
public class MainServ extends HttpServlet{
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)  throws ServletException, IOException {
        try {
            Class.forName("org.postgresql.Driver");
            String url = "jdbc:postgresql://localhost:5432/postgres";
            String login = "postgres";
            String password = "<password>";  /* add here actual pass */
            String func = "{ ? = call aggr.fnc_pb_setinfo(?, ?, ?, ?) }";
            req.setCharacterEncoding("UTF-8");
            String p_gnd = req.getParameter("p_gnd");
            String p_dt  = req.getParameter("p_dt");
            String p_rgn = req.getParameter("p_rgn");
            String p_prf = req.getParameter("p_prf");

            Connection con = DriverManager.getConnection(url, login, password);
            try {
                CallableStatement callableStatement = con.prepareCall(func);
                callableStatement.registerOutParameter(1, Types.VARCHAR);
                callableStatement.setString(2, p_gnd);
                callableStatement.setString(3, p_dt);
                callableStatement.setString(4, p_rgn);
                callableStatement.setString(5, p_prf);

                callableStatement.executeUpdate();

                String result = callableStatement.getString(1);
                System.out.println(result);
            } catch (SQLException e) {
                System.err.format("SQL State: %sn%s", e.getSQLState(), e.getMessage());
                e.printStackTrace();
            }
            finally {
                con.close();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
