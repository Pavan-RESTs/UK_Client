
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import mplcairo
import matplotlib

matplotlib.use("module://mplcairo.tk")

mplcairo.set_options(raqm=False)

font_path = r"Fonts\Tamil Font.TTF"

tamil_font = FontProperties(fname=font_path)

plt.title('எனக்கு', fontproperties=tamil_font)

plt.show()
