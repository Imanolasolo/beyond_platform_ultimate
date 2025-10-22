import sqlite3
import streamlit as st
import pathlib
import sys
import os

# Robust import of db_setup: try package-relative first, fallback to inserting
# project root into sys.path and importing by name. This helps when running
# a small runner script (e.g. `run_admin1.py`) or when the module is imported
# as part of the larger app.
try:
    from .. import db_setup
except Exception:
    project_root = pathlib.Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    import db_setup

DB_NAME = db_setup.DB_NAME


def _safe_rerun():
    """Try available Streamlit rerun APIs in a safe order.

    Some Streamlit versions expose `st.rerun()`, others `st.experimental_rerun()`.
    This helper tries both and otherwise continues silently.
    """
    try:
        # Preferred in newer Streamlit
        if hasattr(st, "rerun"):
            st.rerun()
            return
    except Exception:
        pass
    try:
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
            return
    except Exception:
        pass


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def truncate_text(text, max_length=100):
    if not text:
        return ""
    return text if len(text) <= max_length else text[:max_length] + "..."


def manage_videos():
    st.subheader("Gestión de Charlas (Videos)")
    action = st.selectbox("Acción", ["Listar", "Agregar", "Modificar", "Eliminar"], key="videos_action")

    conn = get_db()
    c = conn.cursor()

    if action == "Listar":
        c.execute("SELECT id, titulo, url, descripcion, likes FROM videos ORDER BY id DESC")
        videos = c.fetchall()
        if videos:
            videos_data = []
            for video in videos:
                videos_data.append({
                    "ID": video["id"],
                    "Título": video["titulo"],
                    "URL": video["url"],
                    "Descripción": truncate_text(video["descripcion"], 80) if video["descripcion"] else "",
                    "Likes": video["likes"] or 0,
                })
            st.table(videos_data)
        else:
            st.info("No hay charlas registradas.")

    elif action == "Agregar":
        with st.form("add_video_form"):
            title = st.text_input("Título de la charla")
            url = st.text_input("URL de la charla")
            description = st.text_area("Descripción")
            submitted = st.form_submit_button("Agregar")
            if submitted:
                try:
                    c.execute("INSERT INTO videos (titulo, url, descripcion, likes) VALUES (?, ?, ?, ?)",
                              (title, url, description, 0))
                    conn.commit()
                    st.success("Charla agregada exitosamente.")
                except sqlite3.Error as e:
                    st.error(f"Error al agregar charla: {e}")

    elif action == "Modificar":
        c.execute("SELECT * FROM videos ORDER BY id DESC")
        videos = c.fetchall()
        if videos:
            video_ids = [video["id"] for video in videos]
            selected_id = st.selectbox("Selecciona el ID de la charla a modificar", video_ids, key="modify_video_select")
            video = next((v for v in videos if v["id"] == selected_id), None)
            if video:
                with st.form("modify_video_form"):
                    title = st.text_input("Nuevo título", value=video["titulo"])
                    url = st.text_input("Nueva URL", value=video["url"])
                    description = st.text_area("Nueva descripción", value=video["descripcion"])
                    submitted = st.form_submit_button("Modificar")
                    if submitted:
                        try:
                            c.execute("UPDATE videos SET titulo = ?, url = ?, descripcion = ? WHERE id = ?",
                                      (title, url, description, video["id"]))
                            conn.commit()
                            st.success("Charla modificada exitosamente.")
                        except sqlite3.Error as e:
                            st.error(f"Error al modificar charla: {e}")
        else:
            st.info("No hay charlas para modificar.")

    elif action == "Eliminar":
        c.execute("SELECT * FROM videos ORDER BY id DESC")
        videos = c.fetchall()
        if videos:
            video_ids = [video["id"] for video in videos]
            selected_id = st.selectbox("Selecciona el ID de la charla a eliminar", video_ids, key="delete_video_select")
            if st.button("Eliminar"):
                try:
                    c.execute("DELETE FROM videos WHERE id = ?", (selected_id,))
                    conn.commit()
                    st.success("Charla eliminada exitosamente.")
                except sqlite3.Error as e:
                    st.error(f"Error al eliminar charla: {e}")
        else:
            st.info("No hay charlas para eliminar.")

    conn.close()


def manage_podcasts():
    st.subheader("Gestión de Podcasts")
    action = st.selectbox("Acción", ["Listar", "Agregar", "Modificar", "Eliminar"], key="podcasts_action")

    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM podcasts ORDER BY id DESC")
        podcasts = c.fetchall()
    except sqlite3.Error as e:
        podcasts = []
        st.error(f"Error al acceder a podcasts: {e}")
    finally:
        try:
            conn.close()
        except Exception:
            pass

    if action == "Listar":
        if podcasts:
            podcasts_data = []
            for podcast in podcasts:
                podcasts_data.append({
                    "ID": podcast["id"],
                    "Título": podcast["titulo"],
                    "URL": podcast["url"],
                    "Descripción": truncate_text(podcast["descripcion"], 80) if podcast["descripcion"] else "",
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
                    c.execute("INSERT INTO podcasts (titulo, descripcion, url) VALUES (?, ?, ?)",
                              (title, description, url))
                    conn.commit()
                    st.success("Podcast agregado exitosamente.")
                except sqlite3.Error as e:
                    st.error(f"Error al agregar podcast: {e}")
                finally:
                    conn.close()

    elif action == "Modificar":
        if podcasts:
            podcast_ids = [podcast["id"] for podcast in podcasts]
            selected_id = st.selectbox("Selecciona el ID del podcast a modificar", podcast_ids, key="modify_podcast_select")
            podcast = next((p for p in podcasts if p["id"] == selected_id), None)
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
                            c.execute("UPDATE podcasts SET titulo=?, descripcion=?, url=? WHERE id=?",
                                      (title, description, url, podcast["id"]))
                            conn.commit()
                            st.success("Podcast modificado exitosamente.")
                        except sqlite3.Error as e:
                            st.error(f"Error al modificar podcast: {e}")
                        finally:
                            conn.close()
        else:
            st.info("No hay podcasts para modificar.")

    elif action == "Eliminar":
        if podcasts:
            podcast_ids = [podcast["id"] for podcast in podcasts]
            selected_id = st.selectbox("Selecciona el ID del podcast a eliminar", podcast_ids, key="delete_podcast_select")
            if st.button("Eliminar"):
                try:
                    conn = get_db()
                    c = conn.cursor()
                    c.execute("DELETE FROM podcasts WHERE id = ?", (selected_id,))
                    conn.commit()
                    st.success("Podcast eliminado exitosamente.")
                except sqlite3.Error as e:
                    st.error(f"Error al eliminar podcast: {e}")
                finally:
                    conn.close()
        else:
            st.info("No hay podcasts para eliminar.")


def manage_beyond_summit():
    st.subheader("Gestión del Evento Beyond Summit")
    action = st.selectbox("Acción", ["Listar", "Agregar/Actualizar", "Eliminar"], key="beyond_action")

    conn = get_db()
    c = conn.cursor()

    if action == "Listar":
        c.execute("SELECT * FROM beyond_summit ORDER BY id DESC")
        events = c.fetchall()
        if events:
            events_data = []
            for ev in events:
                events_data.append({
                    "ID": ev["id"],
                    "Descripción": truncate_text(ev["descripcion"], 120),
                    "Fecha": ev["fecha"],
                    "Hora": ev["hora"],
                })
            st.table(events_data)
        else:
            st.info("No hay eventos registrados.")

    elif action == "Agregar/Actualizar":
        c.execute("SELECT * FROM beyond_summit ORDER BY id DESC")
        events = c.fetchall()
        existing = events[0] if events else None

        with st.form("add_update_event_form"):
            description = st.text_area("Descripción del evento", value=existing["descripcion"] if existing else "")
            date = st.date_input("Fecha del evento", value=existing["fecha"] if existing else None)
            time = st.time_input("Hora del evento", value=existing["hora"] if existing else None)
            submitted = st.form_submit_button("Guardar")
            if submitted:
                try:
                    if existing:
                        c.execute("UPDATE beyond_summit SET descripcion=?, fecha=?, hora=? WHERE id=?",
                                  (description, date.isoformat(), time.strftime('%H:%M:%S'), existing["id"]))
                    else:
                        c.execute("INSERT INTO beyond_summit (descripcion, fecha, hora) VALUES (?, ?, ?)",
                                  (description, date.isoformat(), time.strftime('%H:%M:%S')))
                    conn.commit()
                    st.success("Detalles del evento guardados exitosamente.")
                except sqlite3.Error as e:
                    st.error(f"Error al guardar evento: {e}")

    elif action == "Eliminar":
        c.execute("SELECT * FROM beyond_summit ORDER BY id DESC")
        events = c.fetchall()
        if events:
            event_titles = [f'{ev["id"]} - {truncate_text(ev["descripcion"], 40)}' for ev in events]
            selected = st.selectbox("Selecciona un evento", event_titles, key="delete_event_select")
            if st.button("Eliminar evento"):
                ev_id = int(selected.split(" - ")[0])
                try:
                    c.execute("DELETE FROM beyond_summit WHERE id = ?", (ev_id,))
                    conn.commit()
                    st.success("Evento eliminado exitosamente.")
                except sqlite3.Error as e:
                    st.error(f"Error al eliminar evento: {e}")
        else:
            st.info("No hay eventos para eliminar.")

    conn.close()


def show():
    st.title("Panel de Administración — CRUD")

    # --- Local admin login for THIS page only ---
    # This uses a page-local session key 'admin1_authenticated' so it does not
    # interfere with the rest of the platform's authentication.
    if not st.session_state.get('admin1_authenticated', False):
        st.info("Inicia sesión como administrador para acceder a este panel.")
        with st.form("admin1_login_form"):
            password = st.text_input("Contraseña de administrador", type="password")
            submitted = st.form_submit_button("Ingresar")
            if submitted:
                # Obtain expected password from Streamlit secrets or environment variable
                expected_password = None
                try:
                    if hasattr(st, "secrets"):
                        # Prefer .get(...) when available (works for dict-like and Secrets)
                        try:
                            expected_password = st.secrets.get("admin_password")
                        except Exception:
                            # fallback to indexing (in case .get is not present)
                            try:
                                expected_password = st.secrets["admin_password"]
                            except Exception:
                                expected_password = None
                except Exception:
                    expected_password = None

                # Environment variable fallback
                if not expected_password:
                    expected_password = os.environ.get("ADMIN_PASSWORD")

                if expected_password is None:
                    st.error("No hay contraseña de administrador configurada. Contacta al administrador.")
                elif password == expected_password:
                    st.session_state['admin1_authenticated'] = True
                    _safe_rerun()
                else:
                    st.error("Contraseña incorrecta.")
        # Stop rendering the rest until authenticated
        return

    # --- Once authenticated, show the CRUD UI ---
    # Put a logout button in the sidebar that only affects this page.
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Cerrar sesión"):
            st.session_state['admin1_authenticated'] = False
            _safe_rerun()

    st.sidebar.title("Secciones")
    section = st.sidebar.selectbox("Selecciona una sección", ["Charlas (Videos)", "Podcasts", "Beyond Summit (Eventos)"])

    if section == "Charlas (Videos)":
        manage_videos()
    elif section == "Podcasts":
        manage_podcasts()
    elif section == "Beyond Summit (Eventos)":
        manage_beyond_summit()
