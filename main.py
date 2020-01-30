import scene
import ui


class SafeArea(scene.ShapeNode):
  def __init__(self,parent_cls):
    super(SafeArea, self).__init__(parent=parent_cls)
    self.parent_cls=parent_cls
    self.touch = None
    
    _xs,_ys=parent_cls.size
    rect =ui.Path.rect(0,0,_xs*.96,_ys*.92)
    self.path = rect
    self.fill_color = 'crimson'
    self.position=parent_cls.size*.5
    
    self.game_wrap = GameWrap(self,fill_color='navy')
    top_set = self.size[1]*.5-self.game_wrap.size[1]*.5
    self.game_wrap.position = (0,top_set)
    
    self.controller_wrap = ControllerWrap(self,fill_color='hotpink',get_height=self.game_wrap.size[1])
    bottom_set = self.controller_wrap.size[1]*.5-self.size[1]*.5
    self.controller_wrap.position = (0,bottom_set)
    
  def touch_began(self,touch):
    check_location = self.point_from_scene(touch.location)
    
    if check_location in (self.frame):
      self.controller_wrap.touch_began(touch)
  def touch_ended(self, touch):
    check_location = self.point_from_scene(touch.location)
    
    if check_location in (self.frame):
      self.controller_wrap.touch_ended(touch)


class GameWrap(scene.ShapeNode):
  def __init__(self,parent_cls,fill_color):
    super(GameWrap, self).__init__(parent=parent_cls)
    self.parent_cls=parent_cls
    self.touch = None
    self.fill_color = str(fill_color)
    _xs,_ys = self.parent_cls.size
    self.rect = ui.Path.rect(0,0,_xs,_ys*.78125)
    self.path = self.rect
    self.fill_color = str(fill_color)
    


class ControllerWrap(scene.ShapeNode):
  def __init__(self,parent_cls,fill_color,get_height):
    super(ControllerWrap, self).__init__(parent=parent_cls)
    self.parent_cls=parent_cls
    self.touch = None
    self.fill_color = str(fill_color)
    self.get_height = get_height
    _xs,_ys = self.parent_cls.size
    self.rect = ui.Path.rect(0,0,_xs,_ys-self.get_height)
    self.path = self.rect
    
    self.controller_area = ControllerArea(self,fill_color='goldenrod')
  
  def touch_began(self,touch):
    check_location = self.point_from_scene(touch.location)
    
    if check_location in (self.frame):
      self.controller_area.touch_began(touch)
    
  def touch_ended(self, touch):
    check_location = self.point_from_scene(touch.location)
    
    if check_location in (self.frame):
      self.controller_area.touch_ended(touch)
    

class ControllerArea(scene.ShapeNode):
  def __init__(self,parent_cls,fill_color):
    super(ControllerArea, self).__init__(parent=parent_cls)
    self.parent_cls=parent_cls
    self.touch = None
    
    _xs,_ys = self.parent_cls.size
    self.rect = ui.Path.rect(0,0,_xs*.64,_ys*.8)
    self.path = self.rect
    self.fill_color = str(fill_color)
    
    self.top_btn = Button(self,fill_color='navy')
    self.btm_btn = Button(self,fill_color='darkgreen')
    self.lft_btn = Button(self,fill_color='tomato')
    self.rgt_btn = Button(self,fill_color='slateblue')
    
    self.top_btn.position = (0,(self.top_btn.size[1]))
    self.btm_btn.position = (0,-(self.btm_btn.size[1]))
    self.lft_btn.position = (-(self.lft_btn.size[0]),0)
    self.rgt_btn.position = ((self.rgt_btn.size[0]),0)
    
  def touch_began(self,touch):
    check_location = self.point_from_scene(touch.location)
    
    if check_location in (self.frame):
      self.top_btn.touch_began(touch)
      self.btm_btn.touch_began(touch)
      self.lft_btn.touch_began(touch)
      self.rgt_btn.touch_began(touch)
  def touch_ended(self, touch):
    check_location = self.point_from_scene(touch.location)
    
    if check_location in (self.frame):
      self.top_btn.touch_ended(touch)
      self.btm_btn.touch_ended(touch)
      self.lft_btn.touch_ended(touch)
      self.rgt_btn.touch_ended(touch)



class Button(scene.ShapeNode):
  def __init__(self,parent_cls,fill_color):
    super(Button, self).__init__(parent=parent_cls)
    self.parent_cls=parent_cls
    self.touch = None
    self.default_color = str(fill_color)
    self.fill_color = self.default_color
    self.path = ui.Path.oval(0,0,50,50)
  
  def touch_began(self,touch):
    print('きた')
    check_location = self.point_from_scene(touch.location)
    
    if check_location in (self.frame):
      self.fill_color='steelblue'
  
  def touch_ended(self, touch):
    check_location = self.point_from_scene(touch.location)
    
    if check_location in (self.frame):
      self.fill_color=self.default_color


class MainScene(scene.Scene):
  def setup(self):
    self.background_color='gray'
    self.safe_area=SafeArea(self)
    GuideLine(self)

  def update(self):
    pass

  def touch_began(self,touch):
    self.safe_area.touch_began(touch)
  def touch_ended(self, touch):
    self.safe_area.touch_ended(touch)

# アタリ線
class GuideLine(scene.Node):
  def __init__(self,parent_cls):
    super(GuideLine, self).__init__(parent=parent_cls)
    _xs,_ys=parent_cls.size
    ypath = ui.Path()
    xpath = ui.Path()
    ypath.line_to(0,_ys)
    xpath.line_to(_xs,0)
    ypath.line_width = xpath.line_width = 1
    self.yy = scene.ShapeNode(ypath,parent=self,stroke_color='red',position=(_xs*.5, _ys*.5))
    self.xx = scene.ShapeNode(xpath,parent=self,stroke_color='red',position=(_xs*.5, _ys*.5))

main = MainScene()
scene.run(main,
          orientation='PORTRAIT',
          frame_interval=2,
          show_fps=True)

