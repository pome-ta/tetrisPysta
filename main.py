import scene
import ui

# 書き分け
# - colour
# - position
class Button(scene.ShapeNode):
  def __init__(self,main_cls,fill_color):
    super(Button, self).__init__(parent=main_cls)
    self.main_cls=main_cls
    self.touch = None
    self.fill_color = str(fill_color)
    self.path = ui.Path.oval(0,0,50,50)
    #self.position = (main_cls.size)/2
  
  def touch_began(self,touch):
    
    p2s_s=self.point_to_scene(self.frame)
    p4s_s=self.point_from_scene(self.frame)
    p2s_p=self.point_to_scene(self.main_cls.frame)
    p4s_p=self.point_from_scene(self.main_cls.frame)
    
    rzlt = f'p2s_s:{p2s_s}\np4s_s:{p4s_s}\np2s_p:{p2s_p}\np4s_p:{p4s_p}\n{self.frame}'
    print(rzlt)


class MainScene(scene.Scene):
  def setup(self):
    xs = self.size[0]
    ys = self.size[1]
    rect =ui.Path.rect(0,0,xs*.96,ys*.92)
    safe_area = scene.ShapeNode(rect,fill_color='darkgray')
    safe_area.position=self.size/2
    self.safe_area = safe_area
    self.add_child(self.safe_area)
    ypath = ui.Path()
    xpath = ui.Path()
    ypath.line_to(0,ys)
    xpath.line_to(xs,0)
    ypath.line_width = xpath.line_width = 1
    self.yy = scene.ShapeNode(ypath,parent=self,stroke_color='red',position=(xs/2, ys/2))
    self.xx = scene.ShapeNode(xpath,parent=self,stroke_color='red',position=(xs/2, ys/2))

    self.background_color='crimson'

    game_wrap = scene.ShapeNode(ui.Path.rect(0,0,self.safe_area.size[0],self.safe_area.size[1]/1.28),fill_color='lightgreen')

    up_set=self.safe_area.size[1]/2-game_wrap.size[1]/2

    game_wrap.position=(0,up_set)
    self.game_wrap=game_wrap


    cntr_wrap = scene.ShapeNode(ui.Path.rect(0,0,self.safe_area.size[0],self.safe_area.size[1]-game_wrap.size[1]),fill_color='lightskyblue')

    dn_set=cntr_wrap.size[1]/2-self.safe_area.size[1]/2

    cntr_wrap.position=(0,dn_set)
    self.cntr_wrap=cntr_wrap
    self.safe_area.add_child(self.game_wrap)
    self.safe_area.add_child(self.cntr_wrap)

    cntr_div=scene.ShapeNode(ui.Path.rect(0,0,self.cntr_wrap.size[0]*.64,self.cntr_wrap.size[1]*.8),fill_color='goldenrod')
    self.cntr_div=cntr_div
    self.cntr_wrap.add_child(self.cntr_div)

    cnt_btn=ui.Path.oval(0,0,50,50)

    self.up_cnt=Button(self.cntr_div,'navy')
    self.up_cnt.position=0,self.cntr_div.size[1]/2-self.up_cnt.size[1]/2
    self.dn_cnt=scene.ShapeNode(cnt_btn,fill_color='darkgreen')
    self.dn_cnt.position=0,self.dn_cnt.size[1]/2-self.cntr_div.size[1]/2
    self.lf_cnt=scene.ShapeNode(cnt_btn,fill_color='tomato')
    self.lf_cnt.position=self.lf_cnt.size[0]/2-self.cntr_div.size[0]/2,0
    self.rt_cnt=scene.ShapeNode(cnt_btn,fill_color='slateblue')
    self.rt_cnt.position=self.cntr_div.size[0]/2-self.rt_cnt.size[0]/2,0

    #self.cntr_div.add_child(self.up_cnt)
    self.cntr_div.add_child(self.dn_cnt)
    self.cntr_div.add_child(self.lf_cnt)
    self.cntr_div.add_child(self.rt_cnt)



  def update(self):
    pass

  def did_evaluate_actions(self):
    pass
  def touch_began(self,touch):
    print('main: きた')
    self.up_cnt.touch_began(touch)


main = MainScene()
scene.run(main,
          frame_interval=2,
          show_fps=True)

