from random import randint
from copy import copy
from itertools import product
import scene, ui

main_color = 'darkslategray'
stop_color = 'maroon'


class Block(scene.ShapeNode):
  def __init__(self, row, clo):
    super(Block, self).__init__()
    self.x = row
    self.y = clo
    self.b_pos = [self.x, self.y]
    self.wall = False
    self.fixed = False
    self.alpha = .5
    self.is_default()

  def is_default(self):
    self.fixed = False
    self.fill_color = 'dimgray'

  def is_active(self, color):
    self.fixed = False
    self.fill_color = color

  def is_wall(self):
    self.wall = True
    self.fill_color = 0

  def is_fixed(self):
    self.fixed = True

  def push(self):
    self.fill_color = self.fill_color
    self.fixed = self.fixed
    return self.fill_color, self.fixed

  def get(self, push):
    self.fill_color = push[0]
    self.fixed = push[1]


class SetUpMinos:
  def __init__(self):
    i_rotate = ([[-1, 0], [0, 0], [1, 0], [2, 0]], [[1, -2], [1, -1], [1, 0],
                                                    [1, 1]],
                [[-1, -1], [0, -1], [1, -1], [2, -1]], [[0, -2], [0, -1],
                                                        [0, 0], [0, 1]])
    mino_i = {'name': 'i', 'color': 'cyan', 'rotate': i_rotate}

    o_rotate = ([[0, 0], [0, 1], [1, 0], [1, 1]])
    mino_o = {'name': 'o', 'color': 'yellow', 'rotate': o_rotate}

    s_rotate = ([[-1, 0], [0, 0], [0, 1], [1, 1]], [[0, 1], [0, 0], [1, 0],
                                                    [1, -1]],
                [[-1, -1], [0, -1], [0, 0], [1, 0]], [[-1, 1], [-1, 0], [0, 0],
                                                      [0, -1]])
    mino_s = {'name': 's', 'color': 'green', 'rotate': s_rotate}

    z_rotate = ([[0, 1], [1, 1], [1, 0], [2, 0]], [[1, 0], [1, 1], [2, 2],
                                                   [2, 1]],
                [[0, 2], [1, 2], [1, 1], [2, 1]], [[0, 0], [0, 1], [1, 2],
                                                   [1, 1]])
    mino_z = {'name': 'z', 'color': 'red', 'rotate': z_rotate}

    j_rotate = ([[0, 0], [1, 0], [2, 0], [0, 1]], [[1, 1], [1, 0], [2, 1],
                                                   [1, -1]],
                [[0, 0], [1, 0], [2, -1], [2, 0]], [[1, 1], [1, 0], [0, -1],
                                                    [1, -1]])
    mino_j = {'name': 'j', 'color': 'blue', 'rotate': j_rotate}

    l_rotate = ([[0, 0], [1, 0], [2, 0], [2, 1]], [[1, 1], [1, 0], [2, -1],
                                                   [1, -1]],
                [[0, 0], [1, 0], [0, -1], [2, 0]], [[1, 1], [1, 0], [1, -1],
                                                    [0, 1]])
    mino_l = {'name': 'l', 'color': 'orange', 'rotate': l_rotate}

    t_rotate = ([[0, 0], [1, 0], [2, 0], [1, 1]], [[1, -1], [1, 0], [2, 0],
                                                   [1, 1]],
                [[1, -1], [1, 0], [2, 0], [0, 0]], [[1, -1], [1, 0], [1, 1],
                                                    [0, 0]])
    mino_t = {'name': 't', 'color': 'purple', 'rotate': t_rotate}

    self.mino_list = [mino_i, mino_o, mino_s, mino_z, mino_j, mino_l, mino_t]

  def push(self):
    mino = self.get_list(self.mino_list)
    self.set(mino)
    return mino

  def get_list(self, m_list):
    return m_list[randint(0, len(m_list) - 1)]

  def set(self, mino):
    mino['root'] = [0, 0]
    mino['r_index'] = 0
    if mino['name'] != 'o':
      mino['len'] = len(mino['rotate']) - 1
      mino['unit'] = mino['rotate'][0]
    else:
      mino['len'] = None
      mino['unit'] = mino['rotate']

  def set_root(self, mino, root=None):
    if not root:
      root = mino['root']
    self.pass_root(mino, root)
    self.pass_set(mino)

  def pass_root(self, mino, n_root):
    m_root = mino['root']
    x = m_root[0] + n_root[0]
    y = m_root[1] + n_root[1]
    mino['root'] = [x, y]

  def pass_set(self, mino):
    set = []
    for unit in mino['unit']:
      set.append([x + y for x, y in zip(mino['root'], unit)])
    mino['set'] = set


class ActionMinos:
  def __init__(self):
    self.set_up = SetUpMinos()
    self.down = [0, -1]
    self.left = [-1, 0]
    self.right = [1, 0]

  def set_rotate(self, mino):
    # fixme: 壁際回転要検討
    if mino['name'] != 'o':
      if mino['r_index'] != mino['len']:
        mino['r_index'] += 1
        index = mino['r_index']
        mino['unit'] = mino['rotate'][index]
      else:
        mino['r_index'] = 0
        mino['unit'] = mino['rotate'][0]

  def rotate(self, mino):
    self.set_rotate(mino)
    self.set_up.pass_set(mino)

  def ctrl(self, mino, n):
    root = self.check_ctrl(n)
    self.set_up.set_root(mino, root)

  def check_ctrl(self, n):
    if n == 0: return self.down
    if n == 1: return self.left
    if n == 2: return self.right


class TetrisMain(scene.Node):
  def __init__(self, parent_size):
    super(TetrisMain, self).__init__()
    self.row = 12  #12
    self.clo = 24  #24
    # todo: 大きくなると遅くなる
    self.play_speed = 1
    self.dt = 0.0
    self.parent_x, self.parent_y = parent_size
    self.w = self.parent_x * .80
    self.h = self.parent_y * .72
    self.bw = self.w / self.row
    self.bh = self.h / self.clo

    self.set_up = SetUpMinos()
    self.actn = ActionMinos()

    self.set_x = int(self.row / 2) - 1
    self.set_y = int(self.clo - 3)
    self.set_root = [self.set_x, self.set_y]
    self.wall_bloks = []
    self.fixed_bloks = []
    self.line_x = self.row - 1
    self.line_y = self.clo - 3
    self.end_line = 21
    self.s_point = 0
    self.start()

  def start(self):
    self.create_field()
    self.create_mino()
    self.score_board()

  def create_mino(self):
    mino = self.set_up.push()
    self.set_up.set_root(mino, self.set_root)
    self.color_mino(mino)
    self.mino = mino
    return self.mino

  def create_field(self):
    self.blocks = [[self.setup_blocks(r, c) for c in range(self.clo)]
                   for r in range(self.row)]
    self.x_pos = (self.parent_x * .5 - self.bbox[2] * .5 + self.bw * .5)
    self.y_pos = (self.parent_y * .5 - self.bbox[3] * .38 + self.bh * .5)
    self.position = (self.x_pos, self.y_pos)

  def setup_blocks(self, r, c):
    block = Block(r, c)
    wh = min(self.bw, self.bh)
    '''
    # todo: こちらでも可
    path = ui.Path.rounded_rect
    block.path = path(0, 0,
                 wh, wh, 8)
    '''
    block.path = ui.Path.rect(0, 0, wh, wh)
    block.line_width = 1
    block.stroke_color = main_color
    block.position = (block.x * self.bw, block.y * self.bh)
    self.set_wall(block)
    # top の2行消す
    if not (block.y > self.clo - 3):
      self.add_child(block)
    #self.add_child(block)

    # todo: debug 用 (座標出す)
    num = scene.LabelNode(f'{r},{c}', font=('Ubuntu Mono', 10))
    num.color = 1
    num.alpha = 1
    block.add_child(num)
    return block

  def set_wall(self, block):
    if block.x < 3:
      if block.y > self.end_line - 1 or block.x == 0:
        self.wall_bloks.append(block.b_pos)
        block.is_wall()
    if block.x > self.row - 4:
      if block.y > self.end_line - 1 or block.x == self.row - 1:
        self.wall_bloks.append(block.b_pos)
        block.is_wall()
    if block.y == 0:
      self.wall_bloks.append(block.b_pos)
      block.is_wall()

  def color_mino(self, mino, active=True):
    for pos in mino['set']:
      x, y = pos
      if active:
        self.blocks[x][y].is_active(mino['color'])
      else:
        self.blocks[x][y].is_default()

  def hit_action(self, n):
    left = scene.Action.move_by(-2.56, 0, .1)
    right = scene.Action.move_by(2.56, 0, .1)
    if n == 1:
      return scene.Action.sequence(left, right)
    if n == 2:
      return scene.Action.sequence(right, left)

  def move(self, mino, n):
    if not self.is_hit(mino, n):
      self.color_mino(mino, False)
      self.judg_move(mino, n)
      self.color_mino(mino)
    else:
      self.Adjust_pos()
      if n == 0:
        self.run_action(self.fix_down())
        self.set_fix(mino)
      if n == 1: self.run_action(self.hit_action(n))
      if n == 2: self.run_action(self.hit_action(n))

  def is_hit(self, mino, n):
    pre = copy(mino)
    self.judg_move(pre, n)
    return self.check_hit(pre)

  def judg_move(self, mino, n):
    if n != 3:
      self.actn.ctrl(mino, n)
    else:
      self.actn.rotate(mino)

  def check_hit(self, mino):
    fixed = self.wall_bloks + self.fixed_bloks
    for set, fix in product(mino['set'], fixed):
      if set == fix:
        return True
    return False

  def Adjust_pos(self):
    if self.position != (self.x_pos, self.y_pos):
      self.position = (self.x_pos, self.y_pos)

  def fix_down(self):
    down = scene.Action.move_by(0, -2.56, .1)
    up = scene.Action.move_by(0, 2.56, .1)
    return scene.Action.sequence(down, up)

  def down_call(self):
    self.Adjust_pos()
    if not self.is_hit(self.mino, 0):
      self.color_mino(self.mino, False)
      self.set_up.set_root(self.mino, self.actn.down)
      self.color_mino(self.mino)
    else:
      self.run_action(self.fix_down())
      self.set_fix(self.mino)

  def reset(self):
    for x in range(self.row):
      for y in range(self.clo):
        self.blocks[x][y].remove_from_parent()
    self.wall_bloks = []
    self.fixed_bloks = []
    self.s_point = 0
    #self.blocks = []
    self.create_field()

  def set_fix(self, mino):
    for fix in mino['set']:
      if fix[1] == self.end_line:
        self.reset()
        break
      self.fixed_bloks.append(fix)
      x, y = fix
      self.blocks[x][y].is_fixed()
    self.check_line()
    self.mino = self.create_mino()

  def check_line(self):
    for y in range(1, self.line_y):
      fix = []
      if self.blocks[1][y].fixed:
        for x in range(1, self.line_x):
          if self.blocks[x][y].fixed:
            fix.append([x, y])
            if len(fix) == self.row - 2:
              self.clear_line(fix, self.fixed_bloks)
              self.s_point += 1
            else:
              continue
          else:
            continue
      else:
        continue

  def clear_line(self, fix, fixed_blocks):
    for set in fix:
      bx, by = set
      fixed_blocks.remove([bx, by])
      self.blocks[bx][by].is_default()
    self.fall_blocks(by, fixed_blocks)

  def fall_blocks(self, by, fixed_blocks):
    tby = by + 1
    for x in range(1, self.line_x):
      for y in range(tby, self.line_y):
        if y != self.line_y - 1:
          self.blocks[x][y - 1].get(self.blocks[x][y].push())
          if self.blocks[x][y - 1].fixed:
            fixed_blocks.append([x, y - 1])
            fixed_blocks.remove([x, y])
        else:
          self.blocks[x][y].is_default()
    self.check_line()
    self.fixed_bloks = fixed_blocks

  def stop(self):
    if self.play_speed == 1:
      self.play_speed = 500
    else:
      self.play_speed = 1

  def manage_update(self, main_dt):
    self.dt += main_dt
    if self.dt > self.play_speed:
      self.down_call()
      #self.s_point += 1
      self.score.text = f'Score: {self.s_point}'
      self.dt = 0

  def score_board(self):
    self.score = scene.LabelNode()

    self.score.text = f'Score: {self.s_point}'
    self.score.anchor_point = (0, 1)
    self.score.position = (-self.score.size[0] / 2.56,
                           self.w * 2 - self.score.size[1] * 2)
    self.add_child(self.score)


class MainScene(scene.Scene):
  def setup(self):
    self.background_color = 'darkslategray'
    self.df_color = self.background_color
    self.tetris = TetrisMain(self.size)
    #self.mino = self.tetris.mino
    self.add_child(self.tetris)
    # --- btn start
    path = ui.Path.oval(0, 0, 72, 72)
    self.d_btn = scene.ShapeNode(path=path, parent=self, fill_color='white')
    self.d_btn.position = self.size * .5
    self.d_btn.position -= (0, self.size[1] / 2 - self.d_btn.size[1] / 2)
    self.l_btn = scene.ShapeNode(path=path, parent=self, fill_color='red')
    self.l_btn.position = self.size * .5
    self.l_btn.position -= (+(self.l_btn.size[0]),
                            self.size[1] / 2 - self.l_btn.size[1])
    self.r_btn = scene.ShapeNode(path=path, parent=self, fill_color='blue')
    self.r_btn.position = self.size * .5
    self.r_btn.position -= (-(self.r_btn.size[0] * 1),
                            self.size[1] / 2 - self.r_btn.size[1])
    self.e_btn = scene.ShapeNode(path=path, parent=self, fill_color='yellow')
    self.e_btn.position = self.size * .5
    self.e_btn.position -= (0, self.size[1] / 2 - self.e_btn.size[1] * 1.5)

    self.s_btn = scene.ShapeNode(parent=self, fill_color='pink')
    self.s_btn.path = ui.Path.oval(0, 0, 32, 32)
    self.s_btn.position = self.size * .5
    self.s_btn.position -= (self.s_btn.size[0] - self.size[0] / 2,
                            self.size[1] / 3)
    # --- btn end

  def update(self):
    self.tetris.manage_update(self.dt)

  def did_evaluate_actions(self):
    pass

  def touch_began(self, touch):
    # fixme: 長押し処理 🤔
    if touch.location in (self.d_btn.frame):
      self.d_btn.alpha = .256
      self.tetris.move(self.tetris.mino, 0)

    if touch.location in (self.l_btn.frame):
      self.l_btn.alpha = .256
      self.tetris.move(self.tetris.mino, 1)

    if touch.location in (self.r_btn.frame):
      self.r_btn.alpha = .256
      self.tetris.move(self.tetris.mino, 2)

    if touch.location in (self.e_btn.frame):
      self.e_btn.alpha = .256
      self.tetris.move(self.tetris.mino, 3)

    if touch.location in (self.s_btn.frame):
      self.s_btn.alpha = .256
      self.tetris.stop()
      if self.background_color == self.df_color:
        self.background_color = stop_color
        for x in self.tetris.blocks:
          for y in x:
            y.stroke_color = stop_color
      else:
        self.background_color = self.df_color
        for x in self.tetris.blocks:
          for y in x:
            y.stroke_color = main_color

  def touch_ended(self, touch):
    if touch.location in (self.d_btn.frame):
      self.d_btn.alpha = 1
    if touch.location in (self.l_btn.frame):
      self.l_btn.alpha = 1
    if touch.location in (self.r_btn.frame):
      self.r_btn.alpha = 1
    if touch.location in (self.e_btn.frame):
      self.e_btn.alpha = 1
    if touch.location in (self.s_btn.frame):
      self.s_btn.alpha = 1


main = MainScene()
scene.run(main, orientation=1, frame_interval=2, show_fps=True)


