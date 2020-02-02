import scene, ui
import random


class MainScene(scene.Scene):
  def setup(self):
    self.background_color='darkslategray'
    self.default_color = 'seashell'
    _sw, _sh = self.size
    sw = _sw*.88
    sh = _sh*.80
    
    # 10 x 20 のマス
    self.div_x = 10
    self.div_y = 21
    b_w = sw/self.div_x
    b_h = sh/self.div_y
    
    ground = scene.ShapeNode()
    ground.path = ui.Path.rect(0,0,sw,sh)
    ground.alpha = 0
    self.add_child(ground)
    ground.position = self.size*.5
    
    self.blocks = scene.Node()
    self.add_child(self.blocks)
    
    b_x_count = 0
    b_y_count = 0
    
    for block in range(self.div_x*self.div_y):
      block = scene.ShapeNode(fill_color=self.default_color, path=ui.Path.rounded_rect(0,0,b_w,b_h,8), alpha=.5)
      self.blocks.add_child(block)
      block.position = (b_x_count*b_w, b_y_count*b_h)
      b_x_count += 1
      if b_x_count % self.div_x == 0:
        b_y_count += 1
        b_x_count =0

    self.blocks.position = ((self.size - ground.size)*.5) + (block.size*.5)
    
    # todo: 最上部は、終わりフラグ
    self.n = (self.div_x*self.div_y-self.div_x)-int(self.div_x/2)-1
    
    
    #print(self.create_mino(n))
    self.push_mino = self.create_mino(self.n)
    self.post_mino = []
    for i in self.push_mino:
      self.blocks.children[i].fill_color = 'cyan'
      
    self.set_time = 0
    self.end_time = 0
    self.floor_line = [l for l in range(self.div_x)]
    
  def create_mino(self,n):
    minos = [[n,n+1,n+2,n+3], [n,n+1,n+10,n+11],[n,n+1,n+11,n+12], [n+1,n+2,n+10,n+11], [n,n+1,n+2,n+10], [n,n+1,n+2,n+12], [n,n+1,n+2,n+11]]
    randomNum = random.randint(0, 6)
    return minos[randomNum]

  def update(self):
    self.set_time = int(self.t)
    if int(self.t) != 0:
      if self.set_time > self.end_time:
        self.end_time = self.set_time
        
        if not(set(self.floor_line) & set(self.push_mino)):
          
          for i in self.push_mino:
            self.blocks.children[i].fill_color = self.default_color
          self.post_mino = self.push_mino
          self.push_mino =[]
          
          for i in self.post_mino:
            j = i-self.div_x
            self.blocks.children[j].fill_color = 'cyan'
            self.push_mino+=j,
        else:
          self.refloor_line = self.floor_line
          self.floor_line = []
          self.floor_line = list(set(self.refloor_line)|set(self.post_mino))
          print(self.floor_line)
          self.push_mino = self.create_mino(self.n)


main = MainScene()
scene.run(main,
          orientation='PORTRAIT',
          frame_interval=2,
          show_fps=True)



'''
# Tetrimino

mino_I cyan
▪︎▪︎▪︎▪︎

00,01,02,03,04


mino_O yellow
▪︎▪︎
▪︎▪︎
10,11
00,01

mino_S green
 ▪︎▪
︎▪︎▪︎
   11,12
00,01

mino_Z red
▪︎▪︎
 ▪︎▪︎
10,11
   01,02


mino_J blue
▪︎
▪︎▪︎▪︎
10
00,01,02

mino_L orange
  ▪︎
▪︎▪︎▪︎
      
00,01,02,03

mino_T purple
 ▪︎
▪︎▪︎▪︎
   11
00,01,02
'''

