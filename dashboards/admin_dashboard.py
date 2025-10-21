import sqlite3
import streamlit as st

DB_NAME = "db/beyond_platform.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def truncate_text(text, max_length=100):
    """Truncate text to a maximum length with ellipsis."""
    if not text:
        return ""
    return text if len(text) <= max_length else text[:max_length] + "..."

def manage_videos():
    st.subheader("Gestión de Videos")
    action = st.selectbox("Acción", ["Listar", "Agregar", "Modificar", "Eliminar"], key="videos_action")

    conn = get_db()
    c = conn.cursor()

    if action == "Listar":
        c.execute("SELECT id, titulo, url, descripcion, likes FROM videos")
        videos = c.fetchall()
        if videos:
            # Convert to list of dictionaries for better display
            videos_data = []
            for video in videos:
                videos_data.append({
                    "ID": video["id"],
                    "Título": video["titulo"],
                    "URL": video["url"],
                    "Descripción": truncate_text(video["descripcion"], 50) if video["descripcion"] else "",
                    "Likes": video["likes"] or 0
                })
            st.table(videos_data)
        else:
            st.info("No hay videos registrados.")
    
    elif action == "Agregar":
        with st.form("add_video_form"):
            title = st.text_input("Título del video")
            url = st.text_input("URL del video")
            description = st.text_area("Descripción")
            submitted = st.form_submit_button("Agregar")
            if submitted:
                c.execute("INSERT INTO videos (titulo, url, descripcion, likes) VALUES (?, ?, ?, ?)", 
                         (title, url, description, 0))
                conn.commit()
                st.success("Video agregado exitosamente.")
    
    elif action == "Modificar":
        c.execute("SELECT * FROM videos")
        videos = c.fetchall()
        if videos:
            video_titles = [video["titulo"] for video in videos]
            selected_video = st.selectbox("Selecciona un video", video_titles, key="modify_video_select")
            video = next((v for v in videos if v["titulo"] == selected_video), None)
            if video:
                with st.form("modify_video_form"):
                    title = st.text_input("Nuevo título", value=video["titulo"])
                    url = st.text_input("Nueva URL", value=video["url"])
                    description = st.text_area("Nueva descripción", value=video["descripcion"])
                    submitted = st.form_submit_button("Modificar")
                    if submitted:
                        c.execute("UPDATE videos SET titulo = ?, url = ?, descripcion = ? WHERE id = ?",
                                  (title, url, description, video["id"]))
                        conn.commit()
                        st.success("Video modificado exitosamente.")
        else:
            st.info("No hay videos registrados para modificar.")
    
    elif action == "Eliminar":
        c.execute("SELECT * FROM videos")
        videos = c.fetchall()
        if videos:
            video_titles = [video["titulo"] for video in videos]
            selected_video = st.selectbox("Selecciona un video", video_titles, key="delete_video_select")
            if st.button("Eliminar"):
                c.execute("DELETE FROM videos WHERE titulo = ?", (selected_video,))
                conn.commit()
                st.success("Video eliminado exitosamente.")
        else:
            st.info("No hay videos registrados para eliminar.")

    conn.close()

def manage_podcasts():
    st.subheader("Gestión de Podcasts")
    action = st.selectbox("Acción", ["Listar", "Agregar", "Modificar", "Eliminar"], key="podcasts_action")

    # Fetch podcasts from database
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM podcasts ORDER BY id DESC")
        podcasts = c.fetchall()
    except sqlite3.OperationalError:
        podcasts = []
        st.error("Error: La tabla de podcasts no existe en la base de datos.")
    except sqlite3.Error as e:
        podcasts = []
        st.error(f"Error al acceder a la base de datos: {e}")
    finally:
        try:
            conn.close()
        except Exception:
            pass

    if action == "Listar":
        if podcasts:
            # Convert to list of dictionaries for better display
            podcasts_data = []
            for podcast in podcasts:
                podcasts_data.append({
                    "ID": podcast["id"],
                    "Título": podcast["titulo"],
                    "URL": podcast["url"],
                    "Descripción": truncate_text(podcast["descripcion"], 50) if podcast["descripcion"] else "",
                    "Likes": podcast["likes"] or 0
                })
            st.table(podcasts_data)
        else:
            st.info("No hay podcasts registrados.")
    
    elif action == "Agregar":
        with st.form("add_podcast_form"):
            title = st.text_input("Título del podcast")
            url = st.text_input("URL del podcast")
            description = st.text_area("Descripción")
            submitted = st.form_submit_button("Agregar")
            if submitted:
                try:
                    conn = get_db()
                    c = conn.cursor()
                    c.execute("""
                        INSERT INTO podcasts (titulo, descripcion, url, duracion, categoria, likes)
                        VALUES (?, ?, ?, ?, ?, 0)
                    """, (title, description, url, "", ""))
                    conn.commit()
                    st.success("Podcast agregado exitosamente.")
                except sqlite3.Error as e:
                    st.error(f"Error al agregar podcast: {e}")
                finally:
                    conn.close()
    
    elif action == "Modificar":
        if podcasts:
            # Usar claves reales de la DB ('titulo')
            podcast_titles = [podcast["titulo"] for podcast in podcasts]
            selected_podcast = st.selectbox("Selecciona un podcast", podcast_titles, key="modify_podcast_select")
            podcast = next((p for p in podcasts if p["titulo"] == selected_podcast), None)
            if podcast:
                with st.form("modify_podcast_form"):
                    title = st.text_input("Nuevo título", value=podcast["titulo"])
                    url = st.text_input("Nueva URL", value=podcast["url"])
                    description = st.text_area("Nueva descripción", value=podcast["descripcion"])
                    submitted = st.form_submit_button("Modificar")
                    if submitted:
                        try:
                            conn = get_db()
                            c = conn.cursor()
                            c.execute("""
                                UPDATE podcasts 
                                SET titulo=?, descripcion=?, url=?
                                WHERE id=?
                            """, (title, description, url, podcast["id"]))
                            conn.commit()
                            st.success("Podcast modificado exitosamente.")
                        except sqlite3.Error as e:
                            st.error(f"Error al modificar podcast: {e}")
                        finally:
                            conn.close()
        else:
            st.info("No hay podcasts registrados para modificar.")
    
    elif action == "Eliminar":
        if podcasts:
            podcast_titles = [podcast["titulo"] for podcast in podcasts]
            selected_podcast = st.selectbox("Selecciona un podcast", podcast_titles, key="delete_podcast_select")
            if st.button("Eliminar"):
                try:
                    conn = get_db()
                    c = conn.cursor()
                    c.execute("DELETE FROM podcasts WHERE titulo = ?", (selected_podcast,))
                    conn.commit()
                    st.success("Podcast eliminado exitosamente.")
                except sqlite3.Error as e:
                    st.error(f"Error al eliminar podcast: {e}")
                finally:
                    conn.close()
        else:
            st.info("No hay podcasts registrados para eliminar.")

def manage_beyond_summit():
    st.subheader("Gestión del Evento Beyond Summit")
    st.write("Aquí puedes gestionar los detalles del evento Beyond Summit.")
    # Add specific functionality for managing the event as needed
    st.text_area("Descripción del evento", placeholder="Escribe los detalles del evento aquí...")
    st.date_input("Fecha del evento")
    st.time_input("Hora del evento")
    if st.button("Guardar cambios"):
        st.success("Detalles del evento guardados exitosamente.")

def show():
    # Protege el panel si no hay sesión admin (doble chequeo)
    if not st.session_state.get("admin_logged_in", False):
        st.warning("Acceso denegado. Por favor ingresa como administrador.")
        return

    st.sidebar.title("Panel de Administración")
    section = st.sidebar.selectbox("Selecciona una sección", ["Gestión de Videos", "Gestión de Podcasts", "Gestión del Evento Beyond Summit"])

    if section == "Gestión de Videos":
        manage_videos()
    elif section == "Gestión de Podcasts":
        manage_podcasts()
    elif section == "Gestión del Evento Beyond Summit":
        manage_beyond_summit()
