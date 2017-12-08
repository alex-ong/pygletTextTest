import pyglet
import pyglet.window as Window
from pyglet.text import Label
import asyncio
import random
import time
class MyWindow(Window.Window):
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)   
        self.fps_display = Window.FPSDisplay(self)
        self.labels = []
        self.batch = pyglet.graphics.Batch()
    
    def on_draw(self):        
        self.clear()
        self.fps_display.draw()
        for label in self.labels:
            label.refreshValue()
        self.batch.draw()

    def setupLabels(self, valueVars):
        columns = 30
        rows = len(valueVars) // columns
        stringWidth = 50 #pixel gap
        letterHeight = 80
        for row in range(rows):
            for column in range(columns):                
                label = MyLabel(valueVars[column + columns*row],
                                font_name='Consolas',
                                font_size=16,                                  
                                x=column * stringWidth, y=row * letterHeight,
                                anchor_x='left', anchor_y='top',
                                batch=self.batch)
                self.labels.append(label)
        
class ValueVar(object):
    def __init__(self):
        self.value = int(random.random() * 99)
        self.increment = int(random.random() * 5) + 1
    
    def setValue(self):
        self.value += self.increment
        self.value %= 100
        
    def __str__(self):
        return str(self.value).zfill(2)
        
class MyLabel(Label):
    def __init__(self, valueVar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valueVar = valueVar
        
    def draw(self):
        self.refreshValue()
        super().draw()
        
    def refreshValue(self):
        self.text = str(int(random.random() * 99)).zfill(2)
        
class GUI_Main(object):
    def __init__(self):
        self.window = MyWindow(vsync=False,style='borderless',width=1920,height=1080)
    
    def update(self):
        pyglet.clock.tick()
        for window in pyglet.app.windows:
            #window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()
    
    def linkToModel(self, data):
        self.window.setupLabels(data)
        
class Controller(object):
    def __init__(self, items):
        self.items = items

    def update(self):
        for item in self.items:                 
            item.setValue()
            


async def run_tk(view, controller):   
    try:
        startTime = time.time()
        count = 1000
        while count > 0:
            # update gui            
            view.update()      
            # update logic if required.            
            controller.update()            
            count -= 1
    except Exception as e:
        if "application has been destroyed" not in e.args[0]:
            raise     
    endTime = time.time()
    print ("TotalTime:" + str(endTime - startTime))
    print ("time/frame" + str((endTime - startTime)/1000)) 

if __name__ == '__main__':
    gui = GUI_Main()    
    modelVars = [ValueVar() for i in range(600)]        
    controller = Controller(modelVars)
    gui.linkToModel(modelVars)
        # Start running the tkinter update() through an asyncio coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tk(gui, controller))