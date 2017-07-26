
# coding: utf-8

# In[8]:


from __future__ import print_function
from moviepy.editor import *


# In[12]:


clip = (VideoFileClip("cv.mp4")
                .subclip((0,0.0),(1,16))
                .resize(0.6))
clip.write_gif("gif_cv.gif")

