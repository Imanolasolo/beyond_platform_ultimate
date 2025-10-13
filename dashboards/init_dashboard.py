import streamlit as st
import sqlite3

DB_NAME = "db/beyond_platform.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_top_videos(limit=4):
    """Obtiene los videos más votados"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM videos ORDER BY likes DESC LIMIT ?", (limit,))
    videos = c.fetchall()
    conn.close()
    return videos

def get_top_podcasts(limit=4):
    """Obtiene los podcasts más votados"""
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM podcasts ORDER BY likes DESC LIMIT ?", (limit,))
        podcasts = c.fetchall()
    except sqlite3.OperationalError:
        # Si no existe la tabla o columna likes, devolver lista vacía
        podcasts = []
    conn.close()
    return podcasts

def show():
    # Custom CSS for styling
    st.markdown("""
    <style>
    .welcome-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .info-button {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        width: 100%;
        font-size: 16px;
        font-weight: bold;
    }
    
    .info-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #ff5722 0%, #00bcd4 100%);
    }
    
    .info-content {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #667eea;
        display: none;
    }
    
    .info-content.active {
        display: block;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
        background: linear-gradient(135deg, #ff5722 0%, #00bcd4 100%) !important;
    }
    
    /* Eliminar espacios entre columnas para video e imagen */
    .video-image-container [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .video-image-container {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }
    
    /* Ajustar tamaño del video para que coincida con la imagen */
    .video-image-container iframe {
        width: 100% !important;
        height: 400px !important;
        border-radius: 8px;
    }
    
    .video-image-container img {
        width: 100% !important;
        height: 500px !important;
        object-fit: cover !important;
        border-radius: 8px;
    }
    
    /* Caja gris de texto */
    .info-box {
        background-color: #f0f2f6;
        padding: 30px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .info-title {
        font-size: 24px;
        font-weight: bold;
        color: #7c82ce;
        margin-bottom: 15px;
    }
    
    .info-text {
        font-size: 16px;
        color: #555;
        line-height: 1.6;
    }
    
    /* Sección de charlas */
    .charlas-section {
        margin: 40px 0;
    }
    
    .charlas-title {
        font-size: 32px;
        font-weight: bold;
        color: #333;
        text-align: left;
        margin-bottom: 30px;
        text-decoration: underline;
        text-underline-offset: 8px;
    }
    
    .video-thumbnail {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 15px;
    }
    
    .video-thumbnail:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .video-title {
        font-size: 14px;
        font-weight: bold;
        color: #333;
        margin-top: 10px;
        text-align: center;
        line-height: 1.3;
    }
    
    /* Sección de podcasts */
    .podcasts-section {
        margin: 40px 0;
    }
    
    .podcasts-title {
        font-size: 32px;
        font-weight: bold;
        color: #333;
        text-align: left;
        margin-bottom: 30px;
        text-decoration: underline;
        text-underline-offset: 8px;
    }
    
    .podcast-item {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 15px;
        padding: 15px;
        background-color: #f8f9fa;
    }
    
    .podcast-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .podcast-title {
        font-size: 14px;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
        line-height: 1.3;
    }
    
    .no-content-message {
        text-align: center;
        color: #666;
        font-style: italic;
        padding: 40px;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Video y imagen ocupando todo el ancho sin espacios
    st.markdown('<div class="video-image-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1], gap="small")
    with col1:
        # Video más grande usando HTML personalizado
        st.markdown("""
        <iframe width="100%" height="500" src="https://www.youtube.com/embed/ZNn2MBdliow" 
        title="YouTube video player" frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen style="border-radius: 8px;"></iframe>
        """, unsafe_allow_html=True)
            
    with col2:
        st.image("assets/images/image1.jpg", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Caja gris con información
    st.markdown('''
    <div class="info-box">
        <div style="display: flex; align-items: flex-start; gap: 30px;">
            <div style="flex: 1;">
                <div class="info-title">¿QUÉ ES BEYOND PLATFORM?</div>
            </div>
            <div style="flex: 2;">
                <div class="info-text">
                Beyond Platform está pensada para quienes
                creen que la verdadera transformación de las
                sociedades nace de personas apasionadas por
                la educación y la innovación desde diferentes
                puntos de contacto y que son capaces de
                inspirar al mundo con sus acciones
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Sección de Charlas - Videos más votados
    st.markdown('<div class="charlas-section">', unsafe_allow_html=True)
    st.markdown('<div class="charlas-title">CHARLAS</div>', unsafe_allow_html=True)
    
    # Obtener los 4 videos más votados
    top_videos = get_top_videos(4)
    
    if top_videos:
        col1, col2, col3, col4 = st.columns(4)
        columns = [col1, col2, col3, col4]
        
        for i, video in enumerate(top_videos):
            with columns[i]:
                # Extraer ID del video de YouTube
                video_url = video['url']
                if 'youtube.com/watch?v=' in video_url:
                    video_id = video_url.split('watch?v=')[-1].split('&')[0]
                elif 'youtu.be/' in video_url:
                    video_id = video_url.split('youtu.be/')[-1].split('?')[0]
                else:
                    video_id = None
                
                if video_id:
                    # Mostrar miniatura
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                    st.markdown(f'''
                    <div class="video-thumbnail">
                        <a href="{video_url}" target="_blank">
                            <img src="{thumbnail_url}" style="width: 100%; border-radius: 10px;" alt="{video['titulo']}">
                        </a>
                    </div>
                    <div class="video-title">{video['titulo']}</div>
                    ''', unsafe_allow_html=True)
                else:
                    # Fallback si no se puede extraer el ID
                    st.markdown(f"**{video['titulo']}**")
                    st.markdown(f"[Ver video]({video_url})")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Sección de Podcasts - Podcasts más votados
    st.markdown('<div class="podcasts-section">', unsafe_allow_html=True)
    st.markdown('<div class="podcasts-title">PODCASTS</div>', unsafe_allow_html=True)
    
    # Obtener los 4 podcasts más votados
    top_podcasts = get_top_podcasts(4)
    
    if top_podcasts:
        col1, col2, col3, col4 = st.columns(4)
        columns = [col1, col2, col3, col4]
        for i, podcast in enumerate(top_podcasts):
            with columns[i]:
                url = podcast['url']
                is_youtube = ('youtube.com/watch?v=' in url) or ('youtu.be/' in url)
                video_embed = ''
                if is_youtube:
                    if 'youtube.com/watch?v=' in url:
                        video_id = url.split('watch?v=')[-1].split('&')[0]
                    elif 'youtu.be/' in url:
                        video_id = url.split('youtu.be/')[-1].split('?')[0]
                    else:
                        video_id = ''
                    if video_id:
                        video_embed = f'<iframe width="100%" height="180" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius: 8px; margin-bottom: 10px;"></iframe>'
                st.markdown(f'''
                <div class="podcast-item">
                    <div class="podcast-title">{podcast['titulo']}</div>
                    <div style="font-size: 12px; color: #666; margin-bottom: 10px;">
                        {podcast['descripcion'][:60]}{'...' if len(podcast['descripcion']) > 60 else ''}
                    </div>
                    {video_embed if is_youtube else f'<audio controls style="width: 100%; margin: 10px 0;"><source src="{url}" type="audio/mpeg">Tu navegador no soporta el elemento de audio.</audio>'}
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="no-content-message">
            <h3>📻 Próximamente...</h3>
            <p>Estamos preparando contenido de podcast exclusivo para ti. 
            ¡Mantente atento a las actualizaciones!</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Display information based on button clicked (full width)
    if "show_info" in st.session_state:
        st.markdown("---")
        if st.session_state.show_info == "quienes_somos":
            st.markdown("### 🏢 Muyu Education - Quiénes Somos")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Muyu Education** es una empresa dedicada a transformar la educación y el desarrollo personal a través de tecnología innovadora y contenido de alta calidad.
                
                **Nuestra Misión:**
                - 🌱 Facilitar el crecimiento personal y profesional continuo
                - 🌍 Democratizar el acceso a educación de calidad mundial
                - 🤝 Crear comunidades de aprendizaje colaborativo
                """)
            
            with col2:
                st.markdown("""
                **Nuestros Valores:**
                - **Innovación**: Utilizamos tecnología de vanguardia
                - **Calidad**: Contenido curado por expertos
                - **Accesibilidad**: Educación para todos
                - **Comunidad**: Crecimiento conjunto
                
                **🎯 Nuestro Enfoque:**
                Creemos en el poder transformador de la educación cuando se combina con tecnología innovadora y comunidad colaborativa.
                """)
        
        elif st.session_state.show_info == "que_hacemos":
            st.markdown("### 🎯 Qué Hacemos - Nuestra Propuesta")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                **📚 Contenido Curado:**
                - Videos inspiradores de líderes mundiales
                - Podcasts con expertos de diversas industrias
                - Eventos exclusivos con speakers reconocidos
                """)
            
            with col2:
                st.markdown("""
                **🚀 Metodología Innovadora:**
                - Aprendizaje basado en experiencias reales
                - Networking con profesionales de élite
                - Herramientas interactivas de crecimiento
                """)
            
            with col3:
                st.markdown("""
                **🎪 Eventos Beyond Summit:**
                - Conferencias magistrales
                - Workshops prácticos
                - Sesiones de mentoría personalizada
                """)
        
        elif st.session_state.show_info == "que_esperar":
            st.markdown("### ✨ Qué Puedes Esperar - Tu Experiencia")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **🎓 Crecimiento Acelerado:**
                - Acceso a más de 100+ horas de contenido premium
                - Certificaciones reconocidas internacionalmente
                - Mentorías con líderes de la industria
                
                **🌐 Comunidad Global:**
                - Red de contactos de más de 10,000 profesionales
                - Grupos exclusivos por industria y intereses
                - Oportunidades de colaboración internacional
                """)
            
            with col2:
                st.markdown("""
                **🔄 Actualización Constante:**
                - Contenido nuevo cada semana
                - Tendencias y herramientas más actuales
                - Acceso temprano a eventos exclusivos
                
                **📈 Resultados Medibles:**
                - Tracking de tu progreso personal
                - Métricas de crecimiento profesional
                - Retroalimentación personalizada
                """)





