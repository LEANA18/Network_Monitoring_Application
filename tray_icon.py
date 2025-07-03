from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

def upload_image():
    return Image.open("wifi_icon.jpg")


def run_tray(show_callback, quit_callback):
    menu = Menu(
        MenuItem('Show', lambda icon, item: show_callback()),
        MenuItem('Quit', lambda icon, item: quit_callback())
    )
    icon = Icon("NetMon", upload_image(), menu=menu)
    icon.run()