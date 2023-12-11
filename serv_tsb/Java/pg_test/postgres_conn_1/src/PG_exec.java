import java.sql.*;

public class PG_exec {
    public static void main(String[] args) {
        PG_exec p = new PG_exec();
        p.Run_postgres();
    }

    private void Run_postgres() {
        try {
            Class.forName("org.postgresql.Driver");
            String url = "jdbc:postgresql://localhost:5432/postgres";
            String login = "postgres";
            String password = "<password>";
            String func = "{ ? = call aggr.fnc_pb_setinfo(?, ?, ?, ?) }";

            String p_gnd ="Man";
            String p_dt = "19-09-1945";
            String p_rgn ="1";
            String p_prf ="11000.0";
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
