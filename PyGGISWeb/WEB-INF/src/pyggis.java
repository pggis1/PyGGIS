import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Enumeration;


import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


public class pyggis extends HttpServlet {
	public Connection Connect() {
		String url = "jdbc:postgresql://localhost/postgres";
		String user = "postgres";
		String password = "";
		try{ 
		    Class.forName("org.postgresql.Driver"); 
		    } catch (ClassNotFoundException cnfe){ 
		      System.out.println("Could not find the JDBC driver! " + cnfe.getMessage());
		    } 
		Connection conn = null; 
		try { 
		    conn = DriverManager.getConnection 
		                   (url, user, password); 
		     } catch (SQLException sqle) { 
		       System.out.println("Could not connect " + sqle.getMessage());
		     } 
		return conn;
	}

    public void doGet(HttpServletRequest request, 
      HttpServletResponse response)
              throws ServletException, IOException {
    	
    	Enumeration paramNames = request.getParameterNames();
        String parName;
 
        boolean emptyEnum = false;
        if (!paramNames.hasMoreElements()) {
            emptyEnum = true;
        }
        
    	 request.setCharacterEncoding("UTF-8");
    	 
    	 response.setContentType("text/html;charset=UTF-8");
    	 
         PrintWriter writer = response.getWriter();
         writer.println("<html>" +
           		"<head>" +
           		"<title>PyGGIS</title>" +
           		"<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>" +
           		"<style type='text/css'>" +
           		"a:link{text-decoration: none;}" +
           		"a:hover{color:lightblue;}" +
           		"a {outline:none;}" +
           		"td {padding:1px 5px; text-align:center;}" +
           		"td#apple {padding:1px 5px; text-align:left; vertical-align:text-top;}" +
           		"</style>" +  			
           		"</head>" +
           		"<body>");
         if (emptyEnum) {
        	 writer.println(
        			"<a href='?page=horiz'>Горизонты</a><br />" +
              		"<a href='?page=edge'>Бровки</a><br />" +
              		"<a href='?page=body'>Тела</a><br />" +
              		"<a href='?page=isoline'>Изолинии</a><br />" +
              		"<a href='?page=drill'>Скважины</a><br />" +
              		"<a href='?page=sort'>Сорта тел</a><br />" +
              		"<a href='?page=edge_type'>Типы бровок</a><br />" +
              		"<a href='?page=color'>Цвета</a><br />");

         } else {
        	 /*while (paramNames.hasMoreElements()) {
                 parName = (String) paramNames.nextElement();
                 writer.println("<strong>" + parName + "</strong> : " + request.getParameter(parName));
                 writer.println("<br />");
             }
        	 writer.println(request.getParameter("page"));*/
        	 String page = request.getParameter("page");
        	 System.out.println(page);
        	 if (page != null) {
        		 if (page.compareTo("horiz") == 0) {
	        		 Connection conn = this.Connect();
	        		 try {
	        		 Statement st = conn.createStatement();
	
	        		 ResultSet rs = st.executeQuery(
	        		 "select * from horizons;"
	        		 );
	        		 writer.println(
	        				"<table><td>" +
	                   		"<table border='1'>" +
	                   		"<tr><td>id_hor</td><td>point</td><td>h_ledge</td><td>description</td></tr>"
	        				 );
	        		 while (rs.next())
	        		 {
	        			 writer.println(
	        					 "<tr><td><a href='?page=edit_horiz&id=" + rs.getString(1) + "'>" + rs.getString(1)  + "</a></td><td>" 
	        			 + rs.getString(2) + "</td><td>" 
	        			 + rs.getString(3) + "</td><td>"
	        			 + rs.getString(4) + "</td></tr>");
	        		 }
	        		 writer.println(
	                    		"</table></td><td></td>" +
	                    		//"<iframe style='border: 0px solid #FFFFFF;' width='542px' height='420px' src='body.html#" + rs.getString(1) + "'></iframe>" +
	                    		"</table><br/>" +
	        				    "<a href='/pyggis/index'>Назад</a>"
	         				 );
	        		 rs.close();
	        		 st.close();
	        		 } catch (Exception e) {
	        			 writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	        		 }
	        	 }
        		 
        		 if (page.compareTo("edge") == 0) {
	        		 Connection conn = this.Connect();
	        		 try {
	        		 Statement st = conn.createStatement();
	
	        		 ResultSet rs = st.executeQuery(
	        		 "select id_edge,hor,edge_type from edge;"
	        		 );
	        		 writer.println(
	        				"<table><td>" +
	                   		"<table border='1'>" +
	                   		"<tr><td>id_edge</td><td>hor</td><td>edge_type</td></tr>"
	        				 );
	        		 while (rs.next())
	        		 {
	        			 writer.println(
	        					 "<tr><td><a href='?page=edit_edge&id=" + rs.getString(1) + "'>" + rs.getString(1)  + "</a></td><td>" 
	        			 + rs.getString(2) + "</td><td>" 
	        			 + rs.getString(3) + "</td></tr>");
	        		 }
	        		 writer.println(
	                    		"</table></td><td></td>" +
	                    		//"<iframe style='border: 0px solid #FFFFFF;' width='542px' height='420px' src='body.html#" + rs.getString(1) + "'></iframe>" +
	                    		"</table><br/>" +
	        				    "<a href='/pyggis/index'>Назад</a>"
	         				 );
	        		 rs.close();
	        		 st.close();
	        		 } catch (Exception e) {
	        			 writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	        		 }
	        	 }
	        	 
	        	 if (page.compareTo("body") == 0) {
	        		 Connection conn = this.Connect();
	        		 try {
	        		 Statement st = conn.createStatement();
	
	        		 ResultSet rs = st.executeQuery(
	        		 "select id_body,id_hor,h_body,id_sort from body;"
	        		 );
	        		 writer.println(
	                 		"<table border='1'>" +
	        				"<tr><td>id_body</td><td>id_hor</td><td>h_body</td><td>id_sort</td></tr>" 
	      				 );
	        		 while (rs.next())
	        		 {
	        			 writer.println("<tr><td><a href='?page=edit_body&id=" + rs.getString(1) + "'>" + rs.getString(1)  + "</a></td><td>" 
	        					 + rs.getString(2) + "</td><td>" 
	        					 + rs.getString(3) + "</td><td>" 
	        					 + rs.getString(4) + "</td></tr>");
	        		 }
	        		 writer.println(
	        				 	"</table><br/>"
	        				 	+ "<a href='/pyggis/index'>Назад</a>"
	      				 );
	        		 rs.close();
	        		 st.close();
	        		 } catch (Exception e) {
	        			 writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	        		 }
	        	 }
	        	 
	        	 if (page.compareTo("isoline") == 0) {
	        		 Connection conn = this.Connect();
	        		 try {
	        		 Statement st = conn.createStatement();
	
	        		 ResultSet rs = st.executeQuery(
	        		 "select id_topo,heigth,coord_sys from topograph;"
	        		 );
	        		 writer.println(
	                    		"<table border='1'>" +
	                    		"<tr><td>id_topo</td><td>heigth</td><td>coord_sys</td></tr>"		
	         				 );
	        		 while (rs.next())
	        		 {
	        			 writer.println("<tr><td><a href='?page=edit_topo&id=" + rs.getString(1) + "'>" + rs.getString(1)  + "</a></td><td>" 
	        					 + rs.getString(2) + "</td><td>" 
	        					 + rs.getString(3) + "</td></tr>");
	        		 }
	        		 writer.println(
	        				 	"</table><br/>"
	 	        				+ "<a href='/pyggis/index'>Назад</a>"
	         				 );
	        		 rs.close();
	        		 st.close();
	        		 } catch (Exception e) {
	        			 writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	        		 }
	        	 }
	        	 
	        	 if (page.compareTo("drill") == 0) {
	        		 Connection conn = this.Connect();
	        		 try {
	        		 Statement st = conn.createStatement();
	
	        		 ResultSet rs = st.executeQuery(
	        		 "select * from drills;"
	        		 );
	        		 writer.println(
	                   		"<table border='1'>" +
	                   		"<tr><td>id_drill_fld</td><td>horiz</td><td>coord_system</td><td>cords</td><td>type_drill</td></tr>"		
	        				 );
	        		 while (rs.next())
	        		 {
	        			 writer.println("<tr><td><a href='?page=edit_drill&id=" + rs.getString(1) + "'>" + rs.getString(1)  + "</a></td><td>"
	        					 + rs.getString(2) + "</td><td>" 
	        					 + rs.getString(3) + "</td><td>" 
	        					 + rs.getString(4) + "</td><td>" 
	        					 + rs.getString(5) + "</td></tr>"
	        					 );
	        		 }
	        		 writer.println(
	        				 "</table><br/>"
	     	                  + "<a href='?page=add_drill'>Добавить</a>" + " " +
	     	                  "<a href='/pyggis/index'>Назад</a>"
	        				 );
	        		 rs.close();
	        		 st.close();
	        		 } catch (Exception e) {
	        			 writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	        		 }
	        	 }
	        	 
	        	 if (page.compareTo("sort") == 0) {
	        		 Connection conn = this.Connect();
	        		 try {
	        		 Statement st = conn.createStatement();
	
	        		 ResultSet rs = st.executeQuery(
	        		 "select * from sorts;"
	        		 );
	        		 writer.println(
	                  		"<table border='1'>" +
	                  		"<tr><td>id_sort</td><td>name</td><td>norm_weight</td><td>color</td><td>line_type</td><td>thickness</td><td>color_fill</td><td>description</td></tr>"		
	       				 );
	        		 while (rs.next())
	        		 {
	        			 writer.println("<tr><td><a href='?page=edit_sort&id=" + rs.getString(1) + "'>" + rs.getString(1)  + "</a></td><td>" 
	        					 + rs.getString(2) + "</td><td>"  
	        					 + rs.getString(3) + "</td><td>"  
	        					 + rs.getString(4) + "</td><td>"  
	        					 + rs.getString(5) + "</td><td>"  
	        					 + rs.getString(6) + "</td><td>"
	        					 + rs.getString(7) + "</td><td>" 
	        					 + rs.getString(8) + "</td></tr>"
	        					 );
	        		 }
	        		 writer.println(
	        				 "</table><br/>"
	     	                  + "<a href='?page=add_sort'>Добавить</a>" + " " +
	     	                  "<a href='/pyggis/index'>Назад</a>"
	       				 );
	        		 rs.close();
	        		 st.close();
	        		 } catch (Exception e) {
	        			 writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	        		 }
	        	 }
	        	 
	        	 if (page.compareTo("edge_type") == 0) {
	        		 Connection conn = this.Connect();
	        		 try {
	        		 Statement st = conn.createStatement();
	
	        		 ResultSet rs = st.executeQuery(
	        		 "select * from edge_type;"
	        		 );
	        		 writer.println(
	                  		"<table border='1'>" +
	                  		"<tr><td>id_edge_type</td><td>name</td><td>line_type</td><td>color</td><td>thickness</td></tr>"		
	       				 );
	        		 while (rs.next())
	        		 {
	        			 writer.println(
	        					 "<tr><td><a href='?page=edit_edge_type&id=" + rs.getString(1) + "'>" + rs.getString(1)  + "</a></td><td>" 
	        					 + rs.getString(2) + "</td><td>" 
	        					 + rs.getString(3) + "</td><td>" 
	        					 + rs.getString(4) + "</td><td>" 
	        					 + rs.getString(5) + "</td></tr>"
	        					 );
	        		 }
	        		 writer.println(
	                  		"</table><br/>"
	                  		+ "<a href='?page=add_edge_type'>Добавить</a>" + " " +
	                  		"<a href='/pyggis/index'>Назад</a>"
	       				 );
	        		 rs.close();
	        		 st.close();
	        		 } catch (Exception e) {
	        			 writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	        		 }
	        	 }
	        	 
	        	 if (page.compareTo("color") == 0) {
	        		 Connection conn = this.Connect();
	        		 try {
	        		 Statement st = conn.createStatement();
	
	        		 ResultSet rs = st.executeQuery(
	        		 "select * from color;"
	        		 );
	        		 writer.println(
	                 		"<table border='1'>" +
	                 		"<tr><td>id_color</td><td>name_color</td><td>red</td><td>green</td><td>blue</td></tr>"		
	      				 );
	        		 while (rs.next())
	        		 {
	        			 writer.println("<tr><td><a href='?page=edit_color&id=" + rs.getString(1) + "'>" + rs.getString(1)  + "</a></td><td>"
	        					 + rs.getString(2) + "</td><td>"
	        					 + this.ColorCrypt(rs.getString(3)) + "</td><td>"
	        					 + this.ColorCrypt(rs.getString(4)) + "</td><td>"
	        					 + this.ColorCrypt(rs.getString(5)) + "</td></tr>" 
	        					 );
	        		 }
	        		 writer.println(
	        				 "</table><br/>"
	     	                  + "<a href='?page=add_color'>Добавить</a>" + " " +
	     	                  "<a href='/pyggis/index'>Назад</a>"
	       				 );
	        		 rs.close();
	        		 st.close();
	        		 } catch (Exception e) {
	        			 writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	        		 }
	        	 }
	        	 
	        	 if (page.compareTo("add_drill") == 0) {
	        		 writer.println("<html><head></head><body>" +
	        				 "<form name='f_drill' method='POST'>" +
         					 "id_drill_fld = n<br/><br/>"
         					 + "horiz<br/>"
         					 + "<input type='text' name='i1'><br/><br/>"
         					 + "coors_system<br/>"
         					 + "<input type='text' name='i2'><br/><br/>"
         					 + "cords<br/>"
        					 + "<input type='text' name='i3'><br/><br/>"
        					 + "type_drill<br/>"
        					 + "<input type='text' name='i4'><br/><br/>"
        					 + "<input type='hidden' name='type' value='add_drill'>"
        					 + "<input type='submit' name='add' value='Save'></form>"
        					 + "<a href='/pyggis/index?page=drill'>Назад</a>"
        					 + "</body></html>");
	        	 }
	        	 
	        	 if (page.compareTo("add_sort") == 0) {
	        		 writer.println("<html><head></head><body>" +
	        				 "<form name='f_sort' method='POST'>" +
         					 "id_sort = n<br/><br/>"
         					 + "name<br/>"
         					 + "<input type='text' name='i1'><br/><br/>"
         					 + "norm_weight<br/>"
         					 + "<input type='text' name='i2'><br/><br/>"
         					 + "color<br/>"
        					 + "<input type='text' name='i3'><br/><br/>"
        					 + "line_type<br/>"
        					 + "<input type='text' name='i4'><br/><br/>"
        					 + "thickness<br/>"
        					 + "<input type='text' name='i5'><br/><br/>"
        					 + "color_fill<br/>"
        					 + "<input type='text' name='i6'><br/><br/>"
        					 + "description<br/>"
        					 + "<input type='text' name='i7'><br/><br/>"
        					 + "<input type='hidden' name='type' value='add_sort'>"
        					 + "<input type='submit' name='add' value='Save'></form>"
        					 + "<a href='/pyggis/index?page=sort'>Назад</a>"
        					 + "</body></html>");
	        	 }
	        	 
	        	 if (page.compareTo("add_edge_type") == 0) {
	        		 writer.println("<html><head></head><body>" +
	        				 "<form name='f_edge_type' method='POST'>" +
         					 "id_edge_type = n<br/><br/>"
         					 + "name<br/>"
         					 + "<input type='text' name='i1'><br/><br/>"
         					 + "line_type<br/>"
         					 + "<input type='text' name='i2'><br/><br/>"
         					 + "color<br/>"
        					 + "<input type='text' name='i3'><br/><br/>"
        					 + "thickness<br/>"
        					 + "<input type='text' name='i4'><br/><br/>"
        					 + "<input type='hidden' name='type' value='add_edge_type'>"
        					 + "<input type='submit' name='add' value='Save'></form>"
        					 + "<a href='/pyggis/index?page=edge_type'>Назад</a>"
        					 + "</body></html>");
	        	 }
	        	 
	        	 if (page.compareTo("add_color") == 0) {
	        		 writer.println("<html><head></head><body>" +
	        				 "<form name='f_color' method='POST'>" +
         					 "id_color = n<br/><br/>"
         					 + "name_color<br/>"
         					 + "<input type='text' name='i1'><br/><br/>"
         					 + "red<br/>"
         					 + "<input type='text' name='i2'><br/><br/>"
         					 + "green<br/>"
        					 + "<input type='text' name='i3'><br/><br/>"
        					 + "blue<br/>"
        					 + "<input type='text' name='i4'><br/><br/>"
        					 + "<input type='hidden' name='type' value='add_color'>"
        					 + "<input type='submit' name='add' value='Save'></form>"
        					 + "<a href='/pyggis/index?page=color'>Назад</a>"
        					 + "</body></html>");
	        	 }
	        	 
	        	 if (page.compareTo("edit_horiz") == 0) {
	        		 String id = request.getParameter("id");
	        		 Connection conn = this.Connect();
	         		 try {
	         		 Statement st = conn.createStatement();
	
	         		 ResultSet rs = st.executeQuery(
	         		 "select * from horizons where id_hor = " + id + ""
	         		 );
	         		 while (rs.next()) {
	         			 writer.println("<form name='f_horiz' method='POST'>" +
	         					 "id_hor = " + rs.getString(1) + "<br/><br/>"
	         					 + "point<br/>"
	         					 + "<input type='text' value='" + rs.getString(2) + "'><br/><br/>"
	         					 + "h_ledge<br/>"
	         					 + "<input type='text' value='" + rs.getString(3) + "'><br/><br/>"
	         					 + "description<br/>"
	         					 + "<input type='text' value='" + rs.getString(4) + "'><br/><br/>"
	         					 + "<input type='hidden' name='type' value='edit_horiz'>"
	         					 + "<input type='submit' name='edit' value='Save'></form>"
	         					 + "<form name='fd_edge' method='POST'>"
	        					 + "<input type='hidden' name='type' value='del_horiz'>"
	        					 + "<input type='submit' name='del' value='Delete'></br></form>"
	        					 + "<a href='/pyggis/index?page=horiz'>Назад</a>"
	         					 );
	         		 }
	         		 rs.close();
	         		 st.close();
	         		 } catch (Exception e) {
	         			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	         		 }
	        	 }
	        	 
	        	 if (page.compareTo("edit_edge") == 0) {
	        		 String id = request.getParameter("id");
	        		 Connection conn = this.Connect();
	         		 try {
	         		 Statement st = conn.createStatement();
	
	         		 ResultSet rs = st.executeQuery(
	         		 "select id_edge,hor,edge_type from edge where id_edge = " + id + ""
	         		 );
	         		 while (rs.next()) {
	         			 writer.println("<table width='100%'><tr><td id='apple'><form name='f_edge' method='POST'>" +
	         					 "id_edge = " + rs.getString(1) + "<br/><br/>"
	         					 + "hor<br/>"
	         					 + "<input type='text' value='" + rs.getString(2) + "'><br/><br/>"
	         					 + "edge_type<br/>"
	         					 + "<input type='text' value='" + rs.getString(3) + "'><br/><br/>"
	         					 + "<input type='hidden' name='type' value='edit_edge'>"
	         					 + "<input type='submit' name='edit' value='Save'></form>"
	         					 + "<form name='fd_edge' method='POST'>"
	        					 + "<input type='hidden' name='type' value='del_edge'>"
	        					 + "<input type='submit' name='del' value='Delete'></br></form>"
	        					 + "<a href='/pyggis/index?page=edge'>Назад</a>"
	         					 );
	         			writer.println("</td><td>" +
	         					 "<iframe style='border: 0px solid #FFFFFF;' width='542px' height='420px' src='edge.html#" + rs.getString(1) + "'></iframe>"+
	         			 		 "</td></tr></table>"
	         					 );
	         		 }
	         		 rs.close();
	         		 st.close();
	         		 } catch (Exception e) {
	         			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	         		 }
	        	 }
	        	 
	        	 if (page.compareTo("edit_body") == 0) {
	        		 String id = request.getParameter("id");
	        		 Connection conn = this.Connect();
	         		 try {
	         		 Statement st = conn.createStatement();
	
	         		 ResultSet rs = st.executeQuery(
	         		 "select id_body,id_hor,h_body,id_sort from body where id_body = " + id + ""
	         		 );
	         		 while (rs.next()) {
	         			 writer.println("<table width='100%'><tr><td id='apple'><form name='f_body' method='POST'>" +
	         					 "id_body = " + rs.getString(1) + "<br/><br/>"
	         					 + "id_hor<br/>"
	         					 + "<input type='text' value='" + rs.getString(2) + "'><br/><br/>"
	         					 + "h_body<br/>"
	         					 + "<input type='text' value='" + rs.getString(3) + "'><br/><br/>"
	         					 + "id_sort<br/>"
	         					 + "<input type='text' value='" + rs.getString(4) + "'><br/><br/>"
	         					 + "<input type='hidden' name='type' value='edit_body'>"
	         					 + "<input type='submit' name='edit' value='Save'></form>"
	         					 + "<form name='fd_body' method='POST'>"
	        					 + "<input type='hidden' name='type' value='del_body'>"
	        					 + "<input type='submit' name='del' value='Delete'><br/></form>"
	        					 + "<a href='/pyggis/index?page=body'>Назад</a>"
	        					 );
	         			 writer.println("</td><td>" +
	         					 "<iframe style='border: 0px solid #FFFFFF;' width='542px' height='420px' src='body.html#" + rs.getString(1) + "'></iframe>"+
	         			 		 "</td></tr></table>"
	         					 );
	         		 }
	         		 rs.close();
	         		 st.close();
	         		 } catch (Exception e) {
	         			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	         		 }
	        	 }
	        	 
	        	 if (page.compareTo("edit_topo") == 0) {
	        		 String id = request.getParameter("id");
	        		 Connection conn = this.Connect();
	         		 try {
	         		 Statement st = conn.createStatement();
	
	         		 ResultSet rs = st.executeQuery(
	         		 "select id_topo,heigth,coord_sys from topograph where id_topo = " + id + ""
	         		 );
	         		 while (rs.next()) {
	         			 writer.println("<table width='100%'><tr><td id='apple'><form name='f_topo' method='POST'>" +
	         					 "id_topo = " + rs.getString(1) + "<br/><br/>"
	         					 + "heigth<br/>"
	         					 + "<input type='text' value='" + rs.getString(2) + "'><br/><br/>"
	         					 + "coord_sys<br/>"
	         					 + "<input type='text' value='" + rs.getString(3) + "'><br/><br/>"
	         					 + "<input type='hidden' name='type' value='edit_topo'>"
	         					 + "<input type='submit' name='edit' value='Save'></form>"
	         					 + "<form name='fd_topo' method='POST'>"
	        					 + "<input type='hidden' name='type' value='del_topo'>"
	        					 + "<input type='submit' name='del' value='Delete'><br/></form>"
	        					 + "<a href='/pyggis/index?page=topo'>Назад</a>"
	         					 );
	         			writer.println("</td><td>" +
	         					 "<iframe style='border: 0px solid #FFFFFF;' width='542px' height='420px' src='topo.html#" + rs.getString(1) + "'></iframe>"+
	         			 		 "</td></tr></table>"
	         					 );
	         		 }
	         		 rs.close();
	         		 st.close();
	         		 } catch (Exception e) {
	         			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	         		 }
	        	 }
	        	 
	        	 if (page.compareTo("edit_drill") == 0) {
	        		 String id = request.getParameter("id");
	        		 Connection conn = this.Connect();
	         		 try {
	         		 Statement st = conn.createStatement();
	
	         		 ResultSet rs = st.executeQuery(
	         		 "select * from drills where id_drill_fld = " + id + ""
	         		 );
	         		 while (rs.next()) {
	         			 writer.println("<form name='f_drill' method='POST'>" +
	         					 "id_drill_fld = " + rs.getString(1) + "<br/><br/>"
	         					 + "horiz<br/>"
	         					 + "<input type='text' value='" + rs.getString(2) + "'><br/><br/>"
	         					 + "coord_system<br/>"
	         					 + "<input type='text' value='" + rs.getString(3) + "'><br/><br/>"
	         					 + "cords<br/>"
	        					 + "<input type='text' value='" + rs.getString(4) + "'><br/><br/>"
	        					 + "type_drill<br/>"
	        					 + "<input type='text' value='" + rs.getString(5) + "'><br/><br/>"
	        					 + "<input type='hidden' name='type' value='edit_drill'>"
	        					 + "<input type='submit' name='edit' value='Save'></form>"
	        					 + "<form name='fd_drill' method='POST'>"
	        					 + "<input type='hidden' name='type' value='del_drill'>"
	        					 + "<input type='submit' name='del' value='Delete'><br/></form>"
	        					 + "<a href='/pyggis/index?page=drill'>Назад</a>"
	         					 );
	         		 }
	         		 rs.close();
	         		 st.close();
	         		 } catch (Exception e) {
	         			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	         		 }
	        	 }
	        	 
	        	 if (page.compareTo("edit_sort") == 0) {
	        		 String id = request.getParameter("id");
	        		 Connection conn = this.Connect();
	         		 try {
	         		 Statement st = conn.createStatement();
	
	         		 ResultSet rs = st.executeQuery(
	         		 "select * from sorts where id_sort = " + id + ""
	         		 );
	         		 while (rs.next()) {
	         			 writer.println("<form name='f_sort' method='POST'>" +
	         					 "id_sort = " + rs.getString(1) + "<br/><br/>"
	         					 + "name<br/>"
	         					 + "<input type='text' value='" + rs.getString(2) + "'><br/><br/>"
	         					 + "norm_weight<br/>"
	         					 + "<input type='text' value='" + rs.getString(3) + "'><br/><br/>"
	         					 + "color<br/>"
	        					 + "<input type='text' value='" + rs.getString(4) + "'><br/><br/>"
	        					 + "line_type<br/>"
	        					 + "<input type='text' value='" + rs.getString(5) + "'><br/><br/>"
	        					 + "thickness<br/>"
	        					 + "<input type='text' value='" + rs.getString(6) + "'><br/><br/>"
	        					 + "color_fill<br/>"
	        					 + "<input type='text' value='" + rs.getString(7) + "'><br/><br/>"
	        					 + "description<br/>"
	        					 + "<input type='text' value='" + rs.getString(7) + "'><br/><br/>"
	        					 + "<input type='hidden' name='type' value='edit_sort'>"
	        					 + "<input type='submit' name='edit' value='Save'></form>"
	        					 + "<form name='fd_sort' method='POST'>"
	        					 + "<input type='hidden' name='type' value='del_sort'>"
	        					 + "<input type='submit' name='del' value='Delete'><br/></form>"
	        					 + "<a href='/pyggis/index?page=sort'>Назад</a>"
	         					 );
	         		 }
	         		 rs.close();
	         		 st.close();
	         		 } catch (Exception e) {
	         			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	         		 }
	        	 }
	        	 
	        	 if (page.compareTo("edit_edge_type") == 0) {
	        		 String id = request.getParameter("id");
	        		 System.out.println(id);
	        		 Connection conn = this.Connect();
	         		 try {
	         		 Statement st = conn.createStatement();
	
	         		 ResultSet rs = st.executeQuery(
	         		 "select * from edge_type where id_edge_type = " + id + ""
	         		 );
	         		 while (rs.next()) {
	         			 writer.println(
	         					 "<form name='f_edge_type' method='POST'>" +
	         					 "id_edge_type = " + rs.getString(1) + "<br/><br/>"
	         					 + "name<br/>"
	         					 + "<input type='text' name='i1' value='" + rs.getString(2) + "'><br/><br/>"
	         					 + "line_type<br/>"
	         					 + "<input type='text' name='i2' value='" + rs.getString(3) + "'><br/><br/>"
	         					 + "color<br/>"
	        					 + "<input type='text' name='i3' value='" + rs.getString(4) + "'><br/><br/>"
	        					 + "thickness<br/>"
	        					 + "<input type='text' name='i4' value='" + rs.getString(5) + "'><br/><br/>"
	        					 + "<input type='hidden' name='type' value='edit_edge_type'>"
	        					 + "<input type='submit' name='edit' value='Save'></form>"
	        					 + "<form name='fd_edge_type' method='POST'>"
	        					 + "<input type='hidden' name='type' value='del_edge_type'>"
	        					 + "<input type='submit' name='del' value='Delete'><br/></form>"
	        					 + "<a href='/pyggis/index?page=edge_type'>Назад</a>"
	         					 );
	         		 }
	         		 rs.close();
	         		 st.close();
	         		 } catch (Exception e) {
	         			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	         		 }
	        	 }
	        	 
	        	 if (page.compareTo("edit_color") == 0) {
	        		 String id = request.getParameter("id");
	        		 Connection conn = this.Connect();
	         		 try {
	         		 Statement st = conn.createStatement();
	
	         		 ResultSet rs = st.executeQuery(
	         		 "select * from color where id_color = " + id + ""
	         		 );
	         		 while (rs.next()) {
	         			 writer.println("<form name='f_color' method='POST'>" +
	         					 "id_color = " + rs.getString(1) + "<br/><br/>"
	         					 + "name_color<br/>"
	         					 + "<input type='text' name='i1' value='" + rs.getString(2) + "'><br/><br/>"
	         					 + "red<br/>"
	         					 + "<input type='text' name='i2' value='" + this.ColorCrypt(rs.getString(3)) + "'><br/><br/>"
	         					 + "green<br/>"
	        					 + "<input type='text' name='i3' value='" + this.ColorCrypt(rs.getString(4)) + "'><br/><br/>"
	        					 + "blue<br/>"
	        					 + "<input type='text' name='i4' value='" + this.ColorCrypt(rs.getString(5)) + "'><br/><br/>"
	        					 + "<input type='hidden' name='type' value='edit_color'>"
	        					 + "<input type='submit' name='edit' value='Save'></form>"
	        					 + "<form name='fd_color' method='POST'>"
	        					 + "<input type='hidden' name='type' value='del_color'>"
	        					 + "<input type='submit' name='del' value='Delete'><br/></form>"
	        					 + "<a href='/pyggis/index?page=color'>Назад</a>"
	         					 );
	         		 }
	         		 rs.close();
	         		 st.close();
	         		 } catch (Exception e) {
	         			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
	         		 }
	        	 }
        	 }
         }
         writer.println("</body>" +
   		"</html>");
         writer.close();
    }
    
    private String ColorCrypt(String str)  {
    	str = str.substring(2);
    	String res = new String("");
    	for (int i = 0; i < str.length(); i += 2){
    		res+=(char)(Integer.parseInt(str.substring(i, i+2))+18);
    	}
    	return res;
	}

	public void doPost(HttpServletRequest request, 
    	      HttpServletResponse response)
    	              throws ServletException, IOException {
    	    	
    	    	Enumeration paramNames = request.getParameterNames();
    	        String parName;
    	 
    	        boolean emptyEnum = false;
    	        if (!paramNames.hasMoreElements()) {
    	            emptyEnum = true;
    	        }
    	        
    	    	 request.setCharacterEncoding("UTF-8");
    	    	 
    	    	 response.setContentType("text/html;charset=UTF-8");
    	    	 
    	         PrintWriter writer = response.getWriter();
    	         if (request.getParameter("type").compareTo("edit_horiz") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=horiz'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="update horizons set point=" + request.getParameter("i1")
             				 + ",h_ledge=" + request.getParameter("i2")
             				 + ",description='" + request.getParameter("i3") + "' "
             				 + "where id_hor = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("edit_edge") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=edge'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="update edge set hor=" + request.getParameter("i1")
             				 + ",edge_type=" + request.getParameter("i2") + " "
             				 + "where id_edge = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("edit_body") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=body'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="update body set id_hor=" + request.getParameter("i1")
             				 + ",h_body=" + request.getParameter("i2")
             				 + ",id_sort=" + request.getParameter("i3") + " "
             				 + "where id_body = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("edit_topo") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=isoline'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="update topograph set height=" + request.getParameter("i1")
             				 + ",coord_sys=" + request.getParameter("i2") + " "
             				 + "where id_topo = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("edit_drill") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=drill'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="update drills set horiz=" + request.getParameter("i1")
             				 + ",coord_system=" + request.getParameter("i2")
             				 + ",cords=" + request.getParameter("i3")
             				 + ",type_drill=" + request.getParameter("i4") + " "
             				 + "where id_drill_fld = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("edit_sort") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=sort'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="update sorts set name='" + request.getParameter("i1")
             				 + "',norm_weight=" + request.getParameter("i2")
             				 + ",color=" + request.getParameter("i3")
             				 + ",line_type=" + request.getParameter("i4")
             				 + ",thickness=" + request.getParameter("i5")
             				 + ",color_fill=" + request.getParameter("i6")
             				 + ",description='" + request.getParameter("i7") + "' "
             				 + "where id_drill_fld = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("edit_edge_type") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=edge_type'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="update edge_type set name='" + request.getParameter("i1")
             				 + "',line_type=" + request.getParameter("i2")
             				 + ",color=" + request.getParameter("i3")
             				 + ",thickness=" + request.getParameter("i4") + " "
             				 + "where id_edge_type = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("edit_color") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=color'></head><body>");
            		 String id = request.getParameter("id");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="update color set name_color=" + request.getParameter("i1")
             				 + ",red=" + request.getParameter("i2")
             				 + ",green=" + request.getParameter("i3")
             				 + ",blue=" + request.getParameter("i4") + " "
             				 + "where id_color ="+id+";";
             		 writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("del_horiz") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=horiz'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
    	        	 writer.println(id);
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="delete from horiz where id_hor = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>"); 
    	         }
    	         
    	         if (request.getParameter("type").compareTo("del_edge") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=edge'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
    	        	 writer.println(id);
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="delete from edge where id_edge = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>"); 
    	         }
    	         
    	         if (request.getParameter("type").compareTo("del_body") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=body'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
    	        	 writer.println(id);
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="delete from body where id_body = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>"); 
    	         }
    	         
    	         if (request.getParameter("type").compareTo("del_topo") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=topo'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
    	        	 writer.println(id);
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="delete from topograph where id_topo = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>"); 
    	         }
    	         
    	         if (request.getParameter("type").compareTo("del_drill") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=drill'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
    	        	 writer.println(id);
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="delete from drills where id_drill_fld = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>"); 
    	         }
    	         
    	         if (request.getParameter("type").compareTo("del_sort") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=sort'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
    	        	 writer.println(id);
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="delete from sorts where id_sort = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>"); 
    	         }
    	         
    	         if (request.getParameter("type").compareTo("del_edge_type") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=edge_type'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
    	        	 writer.println(id);
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="delete from edge_type where id_edge_type = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>"); 
    	         }
    	         
    	         if (request.getParameter("type").compareTo("del_color") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=color'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
    	        	 String id = request.getParameter("id");
    	        	 writer.println(id);
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="delete from color where id_color = "+id+";";
             		 //writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>"); 
    	         }
    	         
    	         if (request.getParameter("type").compareTo("add_drill") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=drill'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="insert into drills (horiz,coors_system,cords,type_drill) values ('"
             				+ request.getParameter("i1") + "'," + request.getParameter("i2") + ","
             				+ request.getParameter("i3") + "," + request.getParameter("i4") + ");";
             		 writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("add_sort") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=sort'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="insert into sorts (name,norm_weight,color,line_type,thickness,color_fill,description) values ('"
             				+ request.getParameter("i1") + "'," + request.getParameter("i2") + ","
             				+ request.getParameter("i3") + "," + request.getParameter("i4") + "," + request.getParameter("i5")
             				+ "," + request.getParameter("i6") + ",'" + request.getParameter("i7") + "');";
             		 writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("add_edge_type") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=edge_type'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="insert into edge_type (name,line_type,color,thickness) values ('"
             				+ request.getParameter("i1") + "'," + request.getParameter("i2") + ","
             				+ request.getParameter("i3") + "," + request.getParameter("i4") + ");";
             		 writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         if (request.getParameter("type").compareTo("add_color") == 0) {
    	        	 writer.println("<html><head><meta http-equiv='refresh' content='0; url=http://localhost:8080/pyggis/index?page=color'></head><body>");
    	        	 //response.addHeader("Location", "http://localhost:8080/pyggis/pyggis?page=edge_type");
            		 Connection conn = this.Connect();
             		 try {
             		 Statement st = conn.createStatement();
             		 String query="insert into color (name_color,red,green,blue) values ('"
             				+ request.getParameter("i1") + "','" + request.getParameter("i2") + "','"
             				+ request.getParameter("i3") + "','" + request.getParameter("i4") + "');";
             		 writer.println(query);
             		 ResultSet rs = st.executeQuery(
             				 query
             				 );
             		 rs.close();
            		 st.close();
             		 } catch (Exception e) {
             			writer.println("Could not execute query"+e.getMessage()+" "+e.toString());
             		 }
             		 writer.println("</body></html>");
            	 }
    	         
    	         
    }
    
    
}
