import streamlit as st
from preprocessor import preprocess_whatsapp_chat
from helper import fetch_stats, most_busy_users, create_wordcloud, most_common_words, emoji_helper, monthly_timeline, daily_timeline, week_activity_map, month_activity_map, activity_heatmap
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings



# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Custom CSS for animations and styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Remove extra padding and white space */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Main container animations */
    .main {
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Style the sidebar toggle button - KEEP IT VISIBLE */
    [data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Ensure the button SVG icon is visible */
    [data-testid="collapsedControl"] svg {
        color: white !important;
        fill: white !important;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 3rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 3rem;
        animation: slideDown 0.6s ease-out;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .hero-section h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-section p {
        font-size: 1.2rem;
        opacity: 0.95;
        margin-bottom: 1rem;
    }
    
    .hero-image {
        font-size: 6rem;
        margin: 1rem 0;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes slideDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Feature Cards Container */
    .features-container {
        margin: 3rem 0;
    }
    
    .features-title {
        text-align: center;
        color: #667eea;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 2rem;
    }
    
    /* Feature cards - Responsive */
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        border: 2px solid rgba(102, 126, 234, 0.1);
        height: 100%;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    .feature-card h3 {
        color: #667eea;
        font-weight: 700;
        font-size: 1.4rem;
        margin: 1rem 0 0.5rem 0;
    }
    
    .feature-card p {
        color: #2d3748;
        font-size: 1rem;
        line-height: 1.6;
        margin: 0;
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
    }
    
    /* Instructions Section */
    .instructions-section {
        margin: 3rem 0 2rem 0;
    }
    
    .instructions-title {
        text-align: center;
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    .instructions-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 6px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .instructions-box ol {
        color: #2d3748;
        font-size: 1.1rem;
        line-height: 2.2;
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .instructions-box li {
        margin: 0.5rem 0;
    }
    
    .instructions-box strong {
        color: #667eea;
        font-weight: 600;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: scaleIn 0.5s ease-out;
        height: 100%;
        margin-bottom: 1rem;
    }
    
    @keyframes scaleIn {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        animation: slideUp 0.6s ease-out;
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Section titles */
    .section-title {
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        text-align: center;
        position: relative;
        padding-bottom: 1rem;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 1rem;
        margin-top: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .footer p {
        margin: 0.5rem 0;
        font-size: 1rem;
    }
    
    .footer .love {
        color: #ff6b6b;
        animation: heartbeat 1.5s infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        10%, 30% { transform: scale(1.1); }
        20% { transform: scale(0.9); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-section h1 {
            font-size: 1.8rem;
        }
        .hero-section p {
            font-size: 1rem;
        }
        .hero-image {
            font-size: 4rem;
        }
        .features-title, .instructions-title {
            font-size: 1.6rem;
        }
        .section-title {
            font-size: 1.5rem;
        }
    }
    
    /* Hide footer but keep sidebar toggle visible */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)



# Suppress matplotlib font warnings
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

# Set matplotlib styles for emoji support
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")
sns.set_palette("husl")



# Sidebar
st.sidebar.markdown("# 💬 WhatsApp Analyzer")
st.sidebar.markdown("---")



uploaded_file = st.sidebar.file_uploader("📁 Upload Chat File", type=['txt'])



# Welcome screen when no file is uploaded
if uploaded_file is None:
    # Hero Section with Image
    st.markdown("""
    <div class="hero-section">
        <div class="hero-image">💬📊</div>
        <h1>WhatsApp Chat Analyzer</h1>
        <p>Unlock powerful insights from your conversations with beautiful visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown('<h2 class="features-title">✨ Amazing Features</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Detailed Statistics</h3>
            <p>Get comprehensive stats about messages, words, media, and links shared in your chats</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👥</div>
            <h3>User Analysis</h3>
            <p>Discover who's the most active participant in your group conversations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">😊</div>
            <h3>Emoji & Word Insights</h3>
            <p>Explore emoji usage patterns and create stunning word clouds from your messages</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Instructions Section
    st.markdown('<div class="instructions-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="instructions-title">📝 How to Get Started</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="instructions-box">
        <ol>
            <li><strong>Open WhatsApp</strong> on your phone and navigate to the chat you want to analyze</li>
            <li>Tap on the <strong>three dots (⋮)</strong> menu at the top right corner</li>
            <li>Select <strong>More</strong> and then <strong>Export chat</strong></li>
            <li>Choose <strong>Without media</strong> option to export only text messages</li>
            <li>Upload the exported <strong>.txt file</strong> using the sidebar uploader above 👆</li>
            <li>Select a user or choose <strong>Overall</strong> for complete analysis</li>
            <li>Click <strong>Show Analysis</strong> button and enjoy your insights! 🎉</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p style="font-size: 1.2rem;">Built with <span class="love">❤️</span> by <strong>Ayush</strong></p>
        <p style="font-size: 0.9rem; opacity: 0.9;">WhatsApp Chat Analyzer © 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
else:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess_whatsapp_chat(data)
    
    if df.empty:
        st.error("⚠️ Unable to parse the chat file. Please make sure you've uploaded a valid WhatsApp chat export.")
        st.stop()
    
    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox("👤 Show analysis for", user_list)
    
    if st.sidebar.button("🔍 Show Analysis"):
        # Main header
        st.markdown("""
        <div class="hero-section">
            <div class="hero-image">📊</div>
            <h1>Chat Analysis Results</h1>
            <p>Detailed insights from your WhatsApp conversation</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats Area
        num_messages, num_words, num_media_messages, num_links = fetch_stats(selected_user, df)
        
        st.markdown('<h2 class="section-title">📈 Key Statistics</h2>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="font-size: 2.5rem; margin: 0;">💬</h3>
                <h4 style="margin: 0.5rem 0; font-size: 1rem;">Total Messages</h4>
                <h2 style="margin: 0; font-size: 2rem;">{num_messages:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="font-size: 2.5rem; margin: 0;">📝</h3>
                <h4 style="margin: 0.5rem 0; font-size: 1rem;">Total Words</h4>
                <h2 style="margin: 0; font-size: 2rem;">{num_words:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="font-size: 2.5rem; margin: 0;">📷</h3>
                <h4 style="margin: 0.5rem 0; font-size: 1rem;">Media Shared</h4>
                <h2 style="margin: 0; font-size: 2rem;">{num_media_messages:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="font-size: 2.5rem; margin: 0;">🔗</h3>
                <h4 style="margin: 0.5rem 0; font-size: 1rem;">Links Shared</h4>
                <h2 style="margin: 0; font-size: 2rem;">{num_links:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Timelines
        st.markdown('<h2 class="section-title">📅 Timeline Analysis</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📊 Monthly Timeline")
            timeline_data = monthly_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(timeline_data['time'], timeline_data['message'], color='#667eea', linewidth=2.5, marker='o')
            ax.fill_between(timeline_data['time'], timeline_data['message'], alpha=0.3, color='#667eea')
            plt.xticks(rotation=45, ha='right')
            ax.set_xlabel('Time Period', fontsize=12, fontweight='bold')
            ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📈 Daily Timeline")
            daily_data = daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(daily_data['only_date'], daily_data['message'], color='#764ba2', linewidth=2, alpha=0.8)
            plt.xticks(rotation=45, ha='right')
            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Activity Map
        st.markdown('<h2 class="section-title">🗓️ Activity Patterns</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📅 Most Busy Day")
            busy_day = week_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(busy_day.index, busy_day.values, color='#667eea', edgecolor='white', linewidth=2)
            plt.xticks(rotation=45, ha='right')
            ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📆 Most Busy Month")
            busy_month = month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(busy_month.index, busy_month.values, color='#764ba2', edgecolor='white', linewidth=2)
            plt.xticks(rotation=45, ha='right')
            ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Heatmap
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🔥 Weekly Activity Heatmap")
        user_heatmap = activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(14, 6))
        sns.heatmap(user_heatmap, cmap='RdYlGn', linewidths=0.5, linecolor='white', 
                    cbar_kws={'label': 'Message Count'}, annot=False)
        plt.xlabel('Time Period', fontsize=12, fontweight='bold')
        plt.ylabel('Day of Week', fontsize=12, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Most Busy Users (Group level)
        if selected_user == 'Overall':
            st.markdown('<h2 class="section-title">👥 Most Active Users</h2>', unsafe_allow_html=True)
            x, new_df = most_busy_users(df)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.bar(x.index, x.values, color='#667eea', edgecolor='white', linewidth=2)
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom', fontweight='bold')
                plt.xticks(rotation=45, ha='right')
                ax.set_ylabel('Messages', fontsize=12, fontweight='bold')
                ax.set_title('Most Active Users', fontsize=14, fontweight='bold', pad=10)
                ax.grid(axis='y', alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.dataframe(new_df, width='stretch')
                st.markdown('</div>', unsafe_allow_html=True)
        
        # WordCloud
        st.markdown('<h2 class="section-title">☁️ Word Cloud</h2>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        df_wc = create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Most Common Words
        st.markdown('<h2 class="section-title">🔤 Most Common Words</h2>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        most_common_df = most_common_words(selected_user, df)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(most_common_df[0], most_common_df[1], color='#667eea', edgecolor='white', linewidth=1.5)
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2., f' {int(width)}',
                    ha='left', va='center', fontweight='bold', fontsize=10)
        ax.set_xlabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Most Common Words', fontsize=14, fontweight='bold', pad=10)
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Emoji Analysis
        st.markdown('<h2 class="section-title">😊 Emoji Analysis</h2>', unsafe_allow_html=True)
        emoji_df = emoji_helper(selected_user, df)
        
        if not emoji_df.empty:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.dataframe(emoji_df, width='stretch')
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(8, 8))
                top_emojis = emoji_df.head(5)
                sizes = top_emojis[1].values
                labels = [f"{emoji} ({count})" for emoji, count in zip(top_emojis[0].values, sizes)]
                
                colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', 
                         '#fa709a', '#fee140', '#30cfd0', '#a8edea', '#fed6e3']
                explode = tuple([0.05] * len(top_emojis))
                
                wedges, texts, autotexts = ax.pie(
                    sizes, 
                    labels=labels,
                    autopct="%0.1f%%",
                    colors=colors, 
                    startangle=90,
                    explode=explode,
                    shadow=True,
                    textprops={'fontsize': 11, 'weight': 'bold'}
                )
                
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(11)
                    autotext.set_weight('bold')
                
                ax.set_title('Top 5 Most Used Emojis', fontsize=14, fontweight='bold', pad=20)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📭 No emojis found in the selected conversation.")
        
        # Footer
        st.markdown("""
        <div class="footer">
            <p style="font-size: 1.2rem;">Built with <span class="love">❤️</span> by <strong>Ayush</strong></p>
            <p style="font-size: 0.9rem; opacity: 0.9;">WhatsApp Chat Analyzer © 2025</p>
        </div>
        """, unsafe_allow_html=True)