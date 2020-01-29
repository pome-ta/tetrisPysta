# class test
# > 2020/01/28

import scene
import ui


class SubNode(scene.ShapeNode):
  def __init__(self,main_cls):
    super(SubNode, self).__init__(parent=main_cls)
    self.touch = None
    self.path = ui.Path.oval(0,0,200,200)
    self.position = (main_cls.size)/2
  
  def touch_began(self,touch):
    if touch.location in (self.frame):
      print('sub: きた')
    

class MainScene(scene.Scene):
  # `def __init__(self):` つけると死ぬ
  def setup(self):
    self.background_color='crimson'
    self.sub_node=SubNode(self)
    
  def update(self):
    pass
    
  def touch_began(self,touch):
    print('main: きた')
    self.sub_node.touch_began(touch)

main = MainScene()
scene.run(main,
          frame_interval=2,
          show_fps=True)

