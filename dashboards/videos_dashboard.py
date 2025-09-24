import sqlite3
import streamlit as st

DB_NAME = "db/beyond_platform.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def truncate_text(text, max_length=100):
    """Truncate text to a maximum length with ellipsis."""
    return text if len(text) <= max_length else text[:max_length] + "..."

def like_video(video_id):
    """Increment the like count for a video."""
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE videos SET likes = likes + 1 WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()

def get_share_url(video_url):
    """Generate a shareable URL for the video."""
    return video_url

def show():
    # Add custom CSS for tooltip
    st.markdown("""
    <style>
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #333;
        color: white;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 14px;
        line-height: 1.4;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
    }

    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #333 transparent transparent transparent;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

    # Get all videos from database
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM videos ORDER BY likes DESC, descripcion ASC")
    videos = c.fetchall()
    conn.close()

    # Find the video with most likes (first one after ordering)
    main_video = videos[0] if videos else None
    
    col1, col2 = st.columns([3, 6])
    with col1: 
        # Introductory paragraph about Beyond Platform
        st.markdown("""
            **Bienvenido a Beyond Platform**  
            Beyond Platform es un espacio diseñado para inspirar, educar y conectar a las personas a través de contenido multimedia. 
            Aquí encontrarás videos seleccionados cuidadosamente para ayudarte a crecer personal y profesionalmente.
        """)
    with col2:
        if main_video:
            # Show the most liked video as main video
            st.markdown(f"""
                <div style="display: flex; justify-content: center; align-items: center;">
                    <iframe width="320" height="180" 
                            src="{main_video['url'].replace('watch?v=', 'embed/')}" 
                            frameborder="0" 
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            allowfullscreen>
                    </iframe>
                </div>
                <p style="text-align: center; margin-top: 10px; font-style: italic;">
                    Video más popular ({main_video['likes'] or 0} likes)
                </p>
            """, unsafe_allow_html=True)
        else:
            # Fallback to default video if no videos in database
            st.markdown("""
                <div style="display: flex; justify-content: center; align-items: center;">
                    <iframe width="320" height="180" 
                            src="https://www.youtube.com/embed/ZNn2MBdliow" 
                            frameborder="0" 
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            allowfullscreen>
                    </iframe>
                </div>
            """, unsafe_allow_html=True)

    # Add separator line between introduction and videos
    st.markdown("---")

    if videos:
        for i in range(0, len(videos), 3):  # Group videos in sets of 3
            group = videos[i:i+3]
            cols = st.columns(3)  # Create 3 columns for the group
            for col, video in zip(cols, group):
                with col:
                    # Check if description needs truncation
                    description = video['descripcion'] or ""
                    truncated_desc = truncate_text(description)
                    is_truncated = len(description) > 100
                    
                    # Create tooltip HTML if description is truncated
                    if is_truncated:
                        description_html = f"""
                        <div class="tooltip">
                            <span>{truncated_desc}</span>
                            <span class="tooltiptext">{description}</span>
                        </div>
                        """
                    else:
                        description_html = truncated_desc
                    
                    st.markdown(f"""
                        <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                            <iframe width="320" height="180" 
                                    src="{video['url'].replace('watch?v=', 'embed/')}" 
                                    frameborder="0" 
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                    allowfullscreen>
                            </iframe>
                            <p style="margin-top: 10px; text-align: center;">{description_html}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Like and Share buttons
                    button_col1, button_col2 = st.columns(2)
                    with button_col1:
                        if st.button(f"❤️ Like ({video['likes'] or 0})", key=f"like_{video['id']}"):
                            like_video(video['id'])
                            st.rerun()
                    with button_col2:
                        if st.button("📤 Share", key=f"share_{video['id']}"):
                            share_url = get_share_url(video['url'])
                            st.success(f"URL para compartir: {share_url}")
                            st.code(share_url)
            st.markdown("---")  # Add a line separator between groups
    else:
        st.info("No hay videos disponibles.")