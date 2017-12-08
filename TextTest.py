import pyglet
import pyglet.window as Window

import time
class MyWindow(Window.Window):
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)   
        self.fps_display = Window.FPSDisplay(self)
        self.label = pyglet.text.Label('Hello, world',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=self.width//2, y=self.height//2,
                                  anchor_x='center', anchor_y='center')
    
    def on_draw(self):        
        self.clear()
        self.fps_display.draw()
        self.label.draw()    

if __name__ == '__main__':
    win = MyWindow(vsync=False,style='borderless',width=1920,height=1080)
    
    while True:    
        pyglet.clock.tick()    
        t = time.time()
        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()
        print (time.time() - t)    