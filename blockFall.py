import scene, ui


class MainScene(scene.Scene):
  def setup(self):
    self.background_color='darkslategray'
    
    self.default_color = 'seashell'
    _sw, _sh = self.size
    sw = _sw*.92
    sh = _sh*.80
    
    # 10 x 20 のマス
    div_x = 10
    div_y = 20
    b_w = sw/div_x
    b_h = sh/div_y
    '''
    for vx in range(div_x):
      for vy in range(div_y):
    '''
        
    
    
    
    

    ground = scene.ShapeNode()
    ground.path = ui.Path.rect(0,0,sw,sh)
    ground.alpha = 0
    self.add_child(ground)
    ground.position = self.size*.5
    
    self.blocks = scene.Node()
    self.add_child(self.blocks)
    
    b_x_count = 0
    b_y_count = 0
    
    for block in range(div_x*div_y):
      block = scene.ShapeNode(fill_color=self.default_color, path=ui.Path.rounded_rect(0,0,b_w,b_h,8), alpha=.5)
      self.blocks.add_child(block)
      block.position = (b_x_count*b_w, b_y_count*b_h)
      b_x_count += 1
      if b_x_count % div_x == 0:
        b_y_count += 1
        b_x_count =0

    self.blocks.position = ((self.size - ground.size)*.5) + (block.size*.5)
    
    n = (div_x * div_y)-int(div_x/2)-1
    n = 45
    mino_i = [n,n+1,n+2,n+3]
    
    
    self.push_mino = mino_i
    self.post_mino = []
    for i in self.push_mino:
      self.blocks.children[i].fill_color = 'cyan'
      
    self.set_time = 0
    self.end_time = 0
    self.floor_line = [l for l in range(div_x)]
    #print(self.floor_line)
    

  def update(self):
    self.set_time = int(self.t)
    if int(self.t) != 0:
      if self.set_time > self.end_time:
        self.end_time = self.set_time
        
        if not(set(self.floor_line)&set(self.push_mino)):
          
          for i in self.push_mino:
            self.blocks.children[i].fill_color = self.default_color
          self.post_mino = self.push_mino
          self.push_mino =[]
          
          for i in self.post_mino:
            j = i-10
            self.blocks.children[j].fill_color = 'cyan'
            self.push_mino+=j,
            
        
        
      
      
        
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





