#open anaconda cmd prompt
#cd D:\datapacker0024_mlprojects\whatsapp_chat_analyzer
#D:
#code .   #it will open vs code window
#python --version #it will tell version of python
#conda --version

#first we create a github repository
#first we create an environment and whatever packages i install that all will created here
#step1 : conda create -p venv python==3.12.1 -y              #name of environment is "venv"
#venv created as a folder in the left side and in that folder we can see our all packages and library
#
#step2 : conda activate venv/ #it means we are activating our environment and now i am in venv environment
#
#now we are going to clone our entire github repository that we create and we need to sync it with the github
#so that we will be able to commit our code
#go to github create repository page and step by step run all the cmd under the heading
#..OR CREATE A NEW REPOSITORY ON THE COMMAND LINE
#
#1: git init  #initialise the git #we are going to initialise the empty git repository
#you can find out .git folder in the folders in our environment 
#
#2: git add README.md   #now i will just add my README.md file to the github repository
#before adding let's create one README.md file
#it a file where we can write our discriptions nd all
#
#3.1: git commit -m "first commit"             #in oder to commit it
#we can see all the files changes happening
#
#3.2: git status
#
#now we are going to push this commit to our git hub repository
#4: git branch -M main
#5.1: git remote add origin https://github.com/anujahlawat/whatsapp_chat_analyzer.git
#5.2: git remote -v
#6.1: git push -u origin main
#
#now we will create a ".gitignore:Python" file on our github repository site and commmit changes on the website as well
#why i create this ? some of the file that need not be commited in the github that all will removed
#in oder to check everything is updated on my side 
#6.2: git pull                               #all the updation will happen
#
#now we will do setup.py
#create a new file setup.py 
#create a new file requirements.txt            #it will have all the packages that i really need to install
#                                                while i actually implementing my project
#what is setup.py?
#it is responsible in creating my machine learning applications as a package
#let's write the code required for setup.py
#setup() fn ---> you can think of it like a meta data infomation
#
#now in setup.py we have find_packages()
#now how will it able to find out that how many packages are there and all
#create a new folder "src" i.e. source and inside that folder try to create a file __init__.py
#now in setup.py find_packages() will run and whenever it see "__init__.py" in how many folders then it will 
#directy consider this source as a package itself and it will try to buid this and once it build you can import
#it anywhere you want like we import pandas, numpy
#my entire project devlopment will basically happen in this folder "src"
#
#
#there are scenario where we need to install 100 packages and it is not possible to write all packages in 
#install_requires=['pandas','numpy'] in setup.py 
#so what we do is, we try to build a fn in setup.py
#
#now whenever i run requirements.txt then setup.py should also run to build the package
#for enabling that, we will specifically write "-e ." in the end of requirements.txt
#
#pip install -r reqirements.txt
#
#git add .   #to add new files to the git
#git status
#git commit -m "the second commit"
#git push -u origin main



import streamlit as st

import preprocessor    #preprocessor is a file which we create and it has preprocess fn
import helper
import matplotlib.pyplot as plt

import seaborn as sns

st.sidebar.title("whatsapp chat analyzer")
#streamlit run wapp.py ------> to run a file
#it will take us to a new web page
#now i have to write a code to upload whatsapp chat file
#go to streamlit documentation and find file_uploader in api reference

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # so far i write code to upload text file of whatsapp chat
    # now this file is byte data stream. now we have to convert into string
    data = bytes_data.decode("utf-8")        #convert bytes data into string
    #st.text(data)                           #it will show text file
    df = preprocessor.preprocess(data)       #calling preprocess fn of preprocessor file
                                             #it will preprocess our data
    #st.dataframe(df)                         #dataframe is used as a display fn
    #kisi ko dataframe/messages kyu show krne h

    # in last i have dataframe and now we will start doing analysis

    # i need a drop down menu which contain name of all the chat members
    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')     #bcoz iss naam ka koi user nhi h
    user_list.sort()                           #ascending order
    user_list.insert(0, "overall")              #it shows group level analysis
    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("show analysis"):
        #pass                           #show analysis p click krne p analysis start hoga
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        #now we will start analysis
        #now we will show stats like total msg, no. of words, no. of links, no. of media
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("total messages")
            st.title(num_messages)
        with col2:
            st.header("total words")
            st.title(words)
        with col3:
            st.header("total media messages")
            st.title(num_media_messages)
        with col4:
            st.header("total links shared")
            st.title(num_links)


        #monthly time analysis
        st.title("monthly time based analysis")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily time analysis
        st.title("daily time based analysis")
        d_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(d_timeline['only_date'], d_timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #activity map
        st.title("activity map")

        col1,col2 = st.columns(2)

        with col1:
            st.header("most active day")
            busy_day = helper.week_activity_map(selected_user,df)

            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("most active month")
            busy_month = helper.month_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)


        #activity heatmap for active hours
        st.title("active hours analysis")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # now we will find out most busy/active users
        # this can be done at group level
        # we will build a bar chart
        if selected_user == 'overall':
            st.title("most busy users")
            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)
            with col1:

                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)



        #now we will create wordcloud
        st.title("wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #most common words
        st.title("most common words")
        most_common_df = helper.most_common_words(selected_user,df)

        col1, col2 = st.columns(2)

        with col1:
            fig,ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])   #0 and 1 are column names (see python file)
            plt.xticks(rotation = 'vertical')               #barh means horizontal graph
            st.pyplot(fig)

        with col2:
            st.dataframe(most_common_df)




        #emoji analysis
        st.title("emoji analysis")
        emoji_df = helper.emoji_helper(selected_user,df)

        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="\0.2f") #autopct is to show percentage
            st.pyplot(fig)



