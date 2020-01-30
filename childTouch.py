# child touch テスト
# > 2020/01/29

import scene
import ui


class ParentNode(scene.ShapeNode):
  def __init__(self, parent_cls):
    super(ParentNode, self).__init__(parent=parent_cls)
    _x = parent_cls.size[0]
    _y = parent_cls.size[1]
    rect = ui.Path.rect(0,0,_x*.88,_y*.92)
    self.path = rect
    self.position = (parent_cls.size)/2
    self.fill_color = 'cyan'

    self.sub_node=SubNode(self)
    self.sub_node2=SubNode(self)
    self.sub_node2.position=(0,0)
    

  def touch_began(self, touch):
    check_location = self.point_from_scene(touch.location)
    
    if check_location in (self.sub_node.frame):
      self.sub_node.touch_began(touch)
    
    if check_location in (self.sub_node2.frame):
      self.sub_node2.touch_began(touch)
  
  def touch_ended(self, touch):
    check_location = self.point_from_scene(touch.location)
    
    if check_location in (self.sub_node.frame):
      self.sub_node.touch_ended(touch)
    
    if check_location in (self.sub_node2.frame):
      self.sub_node2.touch_ended(touch)



class SubNode(scene.ShapeNode):
  def __init__(self, parent_cls,):
    super(SubNode, self).__init__(parent=parent_cls)
    self.touch = None
    self.path = ui.Path.oval(0,0,200,200)
    # Scene 以外は真ん中配置 ?
    _x,_y=parent_cls.size
    self.position = (0,-(_y/2-self.size[1]/2))

  def touch_began(self,touch):
    self.fill_color='steelblue'
  def touch_ended(self, touch):
    self.fill_color='white'


class MainScene(scene.Scene):
  # `def __init__(self):` つけると死ぬ
  def setup(self):
    self.background_color='crimson'
    self.parent_node=ParentNode(self)
    r=ui.Path.rect(0,0,200,200)
    self.yy =scene.ShapeNode(path=r,fill_color='gray')
    self.yy.alpha=.5
    self.yy.position=(self.size[0]/2,132)
    self.add_child(self.yy)

  def update(self):
    pass

  def touch_began(self,touch):
    self.parent_node.touch_began(touch)
  def touch_ended(self, touch):
    self.parent_node.touch_ended(touch)



main = MainScene()
scene.run(main,
          frame_interval=2,
          show_fps=True)

