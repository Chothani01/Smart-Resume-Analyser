import streamlit as st
import nltk
import spacy
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

import en_core_web_sm
nlp = en_core_web_sm.load()
 # require for pyresparser

import requests 
import re
import base64
import random
from pyresparser import ResumeParser # library for resume analysis
from pdfminer.high_level import extract_text
import random
import time
from courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos



def fetch_yt_video_title(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            title = re.search(r'<title>(.*?)</title>', response.text)
            if title:
                return title.group(1).replace(" - YouTube", "").strip()
            else:
                return "Could not parse title"
        else:
            return f"Failed to fetch page (Status {response.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"

    
def course_recommender(course_list):
    st.header("**Courses & Certificates🎓 Recommendations**")
    c = 0
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        if c == no_of_reco:
            break
        
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        # f.read() function read pdf in binary form and base64.b64encode(..) encode data into base64 form then we convert in utf-8 form
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    # pdf_display convert base64_pdf in good format at user interface
    st.markdown(pdf_display, unsafe_allow_html=True)

def pdf_reader(file_path):
    text = extract_text(file_path)
    return text

def main():
    st.title("Smart Resume Analyser")
    pdf_file = st.file_uploader("Choose your Resume", type=['pdf'])
    if pdf_file is not None:
        save_image_path = './Uploaded_Resumes/' + pdf_file.name
        # Write pdf in Uploaded_Resumes folder
        with open(save_image_path, "wb") as f:
            f.write(pdf_file.getbuffer())
            
        if st.button('Analyz'):
            
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            
            if resume_data:
                resume_text = pdf_reader(save_image_path) 
                
                st.header("**Resume Analysis**")
                st.success("Hello "+ resume_data['name'])
                st.subheader("**Your Basic Info**")
                
                try:
                    st.text('Name: ',resume_data['name'])
                    st.text('Email: ', resume_data['email'])
                    st.text('Contact: ', resume_data['mobile_number'])
                    st.text('Resume pages: ', str(resume_data['no_of_pages']))
                except:
                    pass
                
                if resume_data['no_of_pages'] == 1:
                    cand_level = 'Fresher'
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',
                                    unsafe_allow_html=True)
                elif resume_data['no_of_pages']  == 2:
                    cand_level = 'Intermediate'
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',
                                    unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >= 3:
                    cand_level = 'Experienced'
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',
                                    unsafe_allow_html=True)
                    
                st.subheader("**Skills Recommendation💡**")
                # Skills shows
                # keywords = st_tags(label='### Skills that you have', 
                #                    text='See our skills recommendation', 
                #                    value=resume_data['skills'], key='1')
                
                st.multiselect(label="### Skills that you have",
                            options=resume_data.get('skills', []),
                            default=resume_data.get('skills', []),
                            key='1'
                                )

                
                # recommendation
                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
                                'streamlit']
                
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                                'javascript', 'angular js', 'c#', 'flask']
                
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                                    'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                                    'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                                    'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                                    'user research', 'user experience'] 
                
                recommended_skills = []
        
                for i in resume_data['skills']:
                    
                    # Data Science recommendation
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        st.success("**Our analysis says you are looking for Data Scienc Jobs**")
                        recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                                'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                                'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                                'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                                                'Streamlit']
                        
                        # st_tags(label='### Recommended skills for you.',
                        #                                text='Recommended skills generated from System',
                        #                                value=recommended_skills, key='2')
                        
                        st.multiselect(label="### Recommended skills for you.",
                                        options=recommended_skills,
                                        default=recommended_skills,
                                        key='2'
                                        )   

                        st.markdown(
                                '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                                unsafe_allow_html=True)
                        course_recommender(ds_course)
                        break
                        
                    # Web Development recommendation
                    elif i.lower() in web_keyword:
                        print(i.lower())
                        st.success("**Our analysis says you are looking for Web Development Jobs**")
                        recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                                                'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                        st.multiselect(label="### Recommended skills for you.",
                                        options=recommended_skills,
                                        default=recommended_skills,
                                        key='3'
                                        )   
                        st.markdown(
                                '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                                unsafe_allow_html=True)
                        course_recommender(web_course)
                        break
                    
                    # Android App Development
                    elif i.lower() in android_keyword:
                        print(i.lower())
                        st.success("**Our analysis says you are looking for Android App Development Jobs**")
                        recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
                                                'Kivy', 'GIT', 'SDK', 'SQLite']
                        st.multiselect(label="### Recommended skills for you.",
                                        options=recommended_skills,
                                        default=recommended_skills,
                                        key='4'
                                        )   
                        st.markdown(
                                '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                                unsafe_allow_html=True)
                        course_recommender(android_course)
                        break
                    
                    # IOS App Development
                    elif i.lower() in ios_keyword:
                        print(i.lower())
                        st.success("**Our analysis says you are looking for IOS App Development Jobs**")
                        recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                                                'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation',
                                                'Auto-Layout']
                        st.multiselect(label="### Recommended skills for you.",
                                        options=recommended_skills,
                                        default=recommended_skills,
                                        key='5'
                                        )   
                        st.markdown(
                                '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                                unsafe_allow_html=True)
                        course_recommender(ios_course)
                        break
                    
                    # Ui-UX Recommendation
                    elif i.lower() in uiux_keyword:
                        print(i.lower())
                        st.success("**Our analysis says you are looking for UI-UX Development Jobs**")
                        recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                                                'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                                                'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
                                                'Solid', 'Grasp', 'User Research']
                        st.multiselect(label="### Recommended skills for you.",
                                        options=recommended_skills,
                                        default=recommended_skills,
                                        key='6'
                                        )   
                        st.markdown(
                                '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                                unsafe_allow_html=True)
                        course_recommender(uiux_course)
                        break
                
                # Resume writing recommendation
                st.subheader("**Resume Tips & Ideas💡**")
                resume_score = 0
                
                if 'Objective' in resume_text:
                    resume_score += 20
                    st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',
                            unsafe_allow_html=True)
                    
                else: 
                    st.markdown(
                            '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add your career objective, it will give your career intension to the Recruiters.</h4>''',
                            unsafe_allow_html=True)
                
                
                if 'Declaration' in resume_text:
                    resume_score += 20
                    st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Delcaration✍/h4>''',
                            unsafe_allow_html=True)
                
                else:
                    st.markdown(
                            '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h4>''',
                            unsafe_allow_html=True)
                
                
                if 'Hobbies' or 'Interests' in resume_text:
                    resume_score += 20
                    st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies⚽</h4>''',
                            unsafe_allow_html=True)
                
                else:
                    st.markdown(
                            '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',
                            unsafe_allow_html=True)
                    
                
                if 'Achievements' in resume_text:
                    resume_score += 20
                    st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements🏅 </h4>''',
                            unsafe_allow_html=True)

                else:
                    st.markdown(
                            '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.</h4>''',
                            unsafe_allow_html=True)

                
                if 'Project' in resume_text:
                    resume_score += 20
                    st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects👨‍💻 </h4>''',
                            unsafe_allow_html=True)

                else:
                    st.markdown(
                            '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.</h4>''',
                            unsafe_allow_html=True)
                
                st.subheader("**Resume Score📝**")
                st.markdown(
                        """
                        <style>
                            .stProgress > div > div > div > div {
                                background-color: #d73b5c;
                            }
                        </style>""",
                        unsafe_allow_html=True,
                    )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score += 1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success("**Your Resume Writing Score: "+str(score)+"**")
                st.warning("**Note: This score is calculated based on the content that you have added in your Resume.**")
                
                # Resume writing video
                st.header("**Bonus Video for Resume Writing Tips💡**")
                resume_vid = random.choice(resume_videos)
                res_vid_title = fetch_yt_video_title(resume_vid)
                st.subheader("✅**"+ res_vid_title +"**")
                st.video(resume_vid)
                
                # Interview Preparation Video
                st.header("**Bonus Video for Interview👨‍💼 Tips💡**")
                interview_vid = random.choice(interview_videos)
                interview_vid_title = fetch_yt_video_title(interview_vid)
                st.subheader("✅ **"+ interview_vid_title +"**")
                st.video(interview_vid)
                
            else:
                st.error("Something went wrong.")
            
if __name__=="__main__":
    main()