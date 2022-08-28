from matplotlib.widgets import RectangleSelector
import matplotlib.patches as patches
import numpy as np
import settings
import matplotlib.pyplot as plt
import spectral


def select_callback(eclick, erelease,source,fig,axs):
    """
    Callback for line selection.

    *eclick* and *erelease* are the press and release events.
    """
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    row_on, row_off,col_on,col_off = int(y1),int(y2),int(x1),int(x2)
    print(f"row_on={row_on}, row_off={row_off}, col_on={col_on}, col_off={col_off}")
    roi = [(row_on, row_off,col_on,col_off)]
    color = tuple(np.random.randint(256, size=3) / 255)
    rect = patches.Rectangle((col_on, row_on), col_off - col_on, row_off - row_on, linewidth=1, edgecolor=color,
                             facecolor='none')
    axs[0].add_patch(rect)
    axs[1].plot(source[row_on, row_off, :].squeeze(),color=color)
    fig.canvas.draw()


def toggle_selector(event):
    print('Key pressed.')
    if event.key == 't':
        for selector in selectors:
            name = type(selector).__name__
            if selector.active:
                print(f'{name} deactivated.')
                selector.set_active(False)
            else:
                print(f'{name} activated.')
                selector.set_active(True)

source = spectral.open_image("92AV3C.lan")

fig0,axs = plt.subplots(1,2,figsize=(10,5))
axs[0].imshow(spectral.get_rgb(source))


selectors = []
fig = plt.figure(constrained_layout=True)
ax = fig.subplots(1)
ax.set_title("Click and drag to draw a rectangle")
ax.imshow(spectral.get_rgb(source))  # plot something
selectors.append(RectangleSelector(
    ax, lambda eclick, erelease: select_callback(eclick, erelease,source,fig0,axs),
    useblit=True,
    button=[1, 3],  # disable middle button
    minspanx=5, minspany=5,
    spancoords='pixels',
    interactive=True
    ))

fig.canvas.draw()
plt.show()
