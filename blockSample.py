import scene, ui

class MainScene(scene.Scene):
  def setup(self):
    self.background_color='darkslategray'
    _sw, _sh = self.size
    sw = _sw*.92
    sh = _sh*.80
    
    # 10 x 20 のマス
    div_x = 10
    div_y = 20
    b_w = sw/div_x
    b_h = sh/div_y

    ground = scene.ShapeNode()
    ground.path = ui.Path.rect(0,0,sw,sh)
    ground.alpha = 0
    self.add_child(ground)
    ground.position = self.size*.5
    
    self.blocks = scene.Node()
    self.add_child(self.blocks)
    
    b_x_count = 0
    b_y_count = 0
    self.default_color = 'seashell'
    for block in range(div_x*div_y):
      block = scene.ShapeNode(fill_color=self.default_color, path=ui.Path.rounded_rect(0,0,b_w,b_h,8), alpha=.5)
      self.blocks.add_child(block)
      block.position = (b_x_count*b_w, b_y_count*b_h)
      b_x_count += 1
      if b_x_count % div_x == 0:
        b_y_count += 1
        b_x_count =0

    self.blocks.position = ((self.size - ground.size)*.5) + (block.size*.5)
    
    
    n = 0
    mino_i = [n,n+1,n+2,n+3]
    n = 5
    mino_o = [n,n+1,n+10,n+11]
    n = 30
    mino_s = [n,n+1,n+11,n+12]
    n = 35
    mino_z = [n+1,n+2,n+10,n+11]
    n = 60
    mino_j = [n,n+1,n+2,n+10]
    n = 65
    mino_l = [n,n+1,n+2,n+12]
    n = 90
    mino_t = [n,n+1,n+2,n+11]
    
    
    
    for i in mino_i:
      self.blocks.children[i].fill_color = 'cyan'
      
    for i in mino_o:
      self.blocks.children[i].fill_color = 'yellow'
      
    for i in mino_s:
      self.blocks.children[i].fill_color = 'green'
      
    for i in mino_z:
      self.blocks.children[i].fill_color = 'red'
      
    for i in mino_j:
      self.blocks.children[i].fill_color = 'blue'
      
    for i in mino_l:
      self.blocks.children[i].fill_color = 'orange'
      
    for i in mino_t:
      self.blocks.children[i].fill_color = 'purple'
      
    
    
    
    self.block_point = []
    
  def update(self):
    pass
    '''
    # block active reset
    if self.block_point:
      for i in self.block_point:
        self.blocks.children[i].fill_color = self.default_color
    self.block_point = []
    
    for i in range(len(self.blocks.children)):
      if i == int(self.t):
        self.blocks.children[i].fill_color = 'tomato'
        self.block_point+=i,
      '''
        
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
         13
00,01,02,03

mino_T purple
 ▪︎
▪︎▪︎▪︎
   11
00,01,02

'''





