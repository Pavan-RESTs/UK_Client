import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font_path = r"Fonts\Tamil Font.TTF" 

tamil_font = FontProperties(fname=font_path) 

sizes = [25, 35, 20, 20]  
labels = ['எனக்கு ', 'மின்விசிறி', 'கலை', 'வாழைப்பழம்']  
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=90)

ax.axis('equal')

for i, autotext in enumerate(autotexts):
    autotext.set_text(labels[i])  
    autotext.set_color("black")  
    autotext.set_fontsize(12)  
    autotext.set_fontproperties(tamil_font)  

for text in texts:
    text.set_fontproperties(tamil_font)

plt.show()