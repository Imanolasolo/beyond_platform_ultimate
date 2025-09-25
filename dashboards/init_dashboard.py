import streamlit as st

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
    </style>
    """, unsafe_allow_html=True)
    
    # Welcome header
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.video("https://www.youtube.com/embed/ZNn2MBdliow")
        
        
            
    with col2:
        st.markdown("""
        <div class="welcome-header">
            <h1>🚀 Bienvenido a Beyond Platform</h1>
            <p>Tu socio de crecimiento personal y profesional</p>
        </div>
        """, unsafe_allow_html=True)

        # Three information buttons in the same column as video
        col1,col2,col3 = st.columns(3, gap="small")
        with col1:
            if st.button("🏢 ¿Quiénes Somos?", key="quienes_somos"):
                st.session_state.show_info = "quienes_somos"

        with col2:
            if st.button("🎯 ¿Qué Hacemos?", key="que_hacemos"):
                st.session_state.show_info = "que_hacemos"

        with col3:
            if st.button("✨ ¿Qué Puedes Esperar?", key="que_esperar"):
                st.session_state.show_info = "que_esperar"

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

    # Call to action section
    st.markdown("---")
    st.markdown("""
    ### 🌟 ¿Listo para Comenzar Tu Transformación?
    
    Explora nuestras secciones y descubre todo lo que tenemos preparado para ti:
    
    - 🎥 **Charlas**: Videos que cambiarán tu perspectiva
    - 🎧 **Podcasts**: Conversaciones que inspiran acción  
    - 🎯 **Beyond Summit**: Eventos que conectan mentes brillantes
    
    ¡Tu crecimiento comienza hoy! 🚀
    """)



