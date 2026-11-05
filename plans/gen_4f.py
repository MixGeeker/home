# 生成四楼平面图（SVG），坐标单位米：x 面宽 0~9（左→右），z 进深 0~10（后墙→临街）
S = 64          # 1 m = 64 px
OX, OY = 110, 120
W, Hh = 9 * S + OX + 110, 10 * S + OY + 150
X = lambda x: OX + x * S
Y = lambda z: OY + z * S
out = []
def rect(x0, x1, z0, z1, cls):
    out.append(f'<rect class="{cls}" x="{X(x0):.1f}" y="{Y(z0):.1f}" width="{(x1-x0)*S:.1f}" height="{(z1-z0)*S:.1f}"/>')
def line(x0, z0, x1, z1, cls):
    out.append(f'<line class="{cls}" x1="{X(x0):.1f}" y1="{Y(z0):.1f}" x2="{X(x1):.1f}" y2="{Y(z1):.1f}"/>')
def text(x, z, t, cls='lbl', anchor='middle', rot=0):
    tr = f' transform="rotate({rot} {X(x):.1f} {Y(z):.1f})"' if rot else ''
    out.append(f'<text class="{cls}" x="{X(x):.1f}" y="{Y(z):.1f}" text-anchor="{anchor}"{tr}>{t}</text>')
def circle(x, z, r, cls):
    out.append(f'<circle class="{cls}" cx="{X(x):.1f}" cy="{Y(z):.1f}" r="{r*S:.1f}"/>')
def door(hx, hz, lx, lz, ex, ez, sweep):
    # 铰链 (hx,hz)，门扇打开后端点 (lx,lz)，关闭时端点 (ex,ez)
    r = ((lx-hx)**2 + (lz-hz)**2) ** 0.5 * S
    line(hx, hz, lx, lz, 'leaf')
    out.append(f'<path class="swing" d="M{X(ex):.1f},{Y(ez):.1f} A{r:.1f},{r:.1f} 0 0 {sweep} {X(lx):.1f},{Y(lz):.1f}"/>')
def window(x0, x1, z, mull):
    rect(x0, x1, z - 0.12, z + 0.12, 'winbg')
    for d in (-0.06, 0, 0.06): line(x0, z + d, x1, z + d, 'win')
    for m in mull: line(m, z - 0.12, m, z + 0.12, 'win')
def windowz(z0, z1, x):
    rect(x - 0.12, x + 0.12, z0, z1, 'winbg')
    for d in (-0.06, 0, 0.06): line(x + d, z0, x + d, z1, 'win')

# ---------- 外墙（含门窗洞口） ----------
def wall_x(z0, z1, x0, x1, gaps, cls):
    cur = x0
    for a, b in gaps: rect(cur, a, z0, z1, cls); cur = b
    rect(cur, x1, z0, z1, cls)
def wall_z(x0, x1, z0, z1, gaps, cls):
    cur = z0
    for a, b in gaps: rect(x0, x1, cur, a, cls); cur = b
    rect(x0, x1, cur, z1, cls)
wall_x(0, 0.24, 0, 9, [(0.5, 1.2), (3.6, 4.8), (6.0, 7.6)], 'ext')
wall_x(9.76, 10, 0, 9, [(0.4, 4.8), (5.9, 8.1)], 'ext')
wall_z(0, 0.24, 0.24, 9.76, [], 'ext')
wall_z(8.76, 9, 0.24, 9.76, [(2.9, 3.9)], 'ext')
window(0.5, 1.2, 0.12, []); window(3.6, 4.8, 0.12, []); window(6.0, 7.6, 0.12, [6.8])
window(0.4, 4.8, 9.88, [1.5, 2.6, 3.7]); window(5.9, 8.1, 9.88, [7.0])
windowz(2.9, 3.9, 8.88)
# ---------- 内墙 ----------
wall_z(1.6, 1.72, 0.24, 2.5, [], 'int')                    # 电梯井左
wall_z(3.28, 3.4, 0.24, 2.5, [(0.9, 1.8)], 'int')          # 电梯井右，电梯门朝电梯厅
wall_x(2.38, 2.5, 1.6, 3.4, [], 'int')                     # 电梯井下
wall_x(2.44, 2.56, 3.4, 5.0, [(4.15, 4.95)], 'int')        # 入户墙
wall_x(2.44, 2.56, 5.0, 8.76, [], 'int')                   # 楼梯间墙
wall_z(2.54, 2.66, 2.5, 9.76, [(7.6, 8.45)], 'int')        # 衣帽卫浴区隔墙（落在窗竖梃 x=2.6）
wall_z(5.94, 6.06, 2.5, 4.5, [(3.5, 4.3)], 'int')          # 客卫
wall_x(4.44, 4.56, 6.0, 8.76, [], 'int')
# ---------- 柱 ----------
for x in (0.2, 5.0, 8.8):
    for z in (0.2, 2.5, 8.5, 9.8):
        if x == 5.0 and z == 9.8: continue
        rect(x - 0.21, x + 0.21, z - 0.21, z + 0.21, 'col')
# ---------- 门 ----------
door(4.15, 2.56, 4.15, 3.36, 4.95, 2.56, 1)               # 入户门
door(2.54, 8.45, 1.74, 8.45, 2.54, 7.6, 0)                # 衣帽间门
door(6.06, 4.3, 6.86, 4.3, 6.06, 3.5, 1)                  # 客卫门
line(3.34, 0.9, 3.34, 1.8, 'slide')                        # 电梯门
# ---------- 楼梯 ----------
rect(5.0, 8.0, 0.26, 1.25, 'stair'); rect(5.0, 8.0, 1.33, 2.44, 'stair'); rect(8.0, 8.76, 0.26, 2.44, 'stair')
for i in range(1, 10):
    x = 5.0 + 0.3 * i; line(x, 0.26, x, 1.25, 'tread'); line(x, 1.33, x, 2.44, 'tread')
line(5.2, 0.75, 7.8, 0.75, 'arrow'); text(5.35, 0.62, '上', 'small', 'start')
line(7.8, 1.9, 5.2, 1.9, 'arrow'); text(5.35, 2.25, '下', 'small', 'start')
# ---------- 电梯 ----------
rect(1.8, 3.2, 0.36, 2.3, 'lift'); line(1.8, 0.36, 3.2, 2.3, 'thin'); line(3.2, 0.36, 1.8, 2.3, 'thin')
# ---------- 家具与设备 ----------
F = 'furn'
rect(0.24, 1.6, 0.24, 1.6, 'wet'); line(0.24, 1.6, 1.6, 1.6, 'glass'); text(0.92, 0.98, '淋浴', 'small')
rect(0.26, 0.94, 1.9, 2.3, F); text(0.6, 2.18, '马桶', 'tiny')
rect(1.99, 2.54, 2.8, 4.2, F); circle(2.27, 3.25, 0.16, 'furn'); circle(2.27, 3.75, 0.16, 'furn'); line(2.52, 2.85, 2.52, 4.15, 'glass')
text(1.86, 3.5, '双人台盆 1400', 'tiny', 'middle', -90)
rect(0.24, 0.99, 2.75, 4.45, F); rect(0.34, 0.89, 2.85, 4.35, 'wet'); text(0.615, 3.6, '浴缸 1700', 'tiny', 'middle', -90)
rect(0.24, 0.84, 5.0, 8.4, 'wood'); text(0.54, 6.7, '衣柜 3400', 'tiny', 'middle', -90)
rect(2.0, 2.54, 5.0, 7.45, 'wood'); text(2.27, 6.2, '衣柜 2450', 'tiny', 'middle', -90)
rect(0.3, 0.92, 8.62, 9.24, F); text(0.61, 8.98, '洗烘', 'tiny')
rect(0.92, 2.0, 8.62, 9.24, F); text(1.46, 8.98, '洗衣池柜', 'tiny')
rect(2.0, 2.54, 8.62, 9.2, F)
line(0.4, 9.42, 2.5, 9.42, 'dash'); line(0.4, 9.66, 2.5, 9.66, 'dash'); text(1.45, 9.6, '晾衣杆', 'tiny')
rect(2.66, 3.11, 2.6, 4.4, 'show'); text(2.885, 3.5, '手办柜', 'tiny', 'middle', -90)
rect(5.5, 5.94, 2.6, 3.4, 'wood'); text(5.72, 3.0, '鞋柜', 'tiny', 'middle', -90)
rect(2.66, 3.26, 4.6, 7.45, 'wood'); rect(2.66, 3.26, 4.62, 5.22, F)
text(2.96, 4.98, '冰箱', 'tiny'); text(2.96, 6.35, '零食柜 / 台面', 'tiny', 'middle', -90)
rect(3.4, 6.0, 4.9, 8.3, 'rug')
rect(3.9, 5.3, 6.7, 7.4, 'wood'); text(4.6, 7.12, '电脑桌 1400×700', 'tiny')
rect(4.3, 4.9, 7.5, 8.1, F); text(4.6, 7.86, '电竞椅', 'tiny')
circle(4.6, 5.6, 0.5, 'spot'); rect(4.1, 5.1, 5.25, 5.95, F); line(3.65, 5.69, 5.55, 5.69, 'tv')
text(4.6, 5.42, '移动支架 85″', 'tiny'); text(4.6, 5.9, '停靠位①', 'tiny')
circle(5.75, 5.9, 0.5, 'spot'); text(5.75, 5.95, '停靠位②', 'tiny')
rect(6.66, 8.76, 5.15, 6.95, F); rect(8.68, 8.76, 5.15, 6.95, 'wood')
rect(8.0, 8.6, 5.3, 5.95, 'pillow'); rect(8.0, 8.6, 6.15, 6.8, 'pillow')
rect(8.31, 8.76, 4.65, 5.1, 'wood'); rect(8.31, 8.76, 7.0, 7.45, 'wood')
text(7.35, 6.12, '床 1800×2100', 'tiny')
rect(2.7, 4.79, 8.6, 9.72, 'wood'); rect(4.79, 5.21, 8.71, 9.72, 'wood'); rect(5.21, 6.5, 8.6, 9.72, 'wood')
text(3.7, 9.25, '实验工作台 3800×1100', 'tiny')
rect(5.6, 6.4, 9.2, 9.65, F); text(6.0, 9.48, '拍照箱', 'tiny')
rect(8.31, 8.76, 7.6, 9.76, 'show'); text(8.535, 8.7, '到顶手办柜', 'tiny', 'middle', -90)
circle(7.25, 9.45, 0.25, 'plant')
rect(6.1, 6.6, 2.65, 3.25, F); rect(7.4, 7.8, 2.51 + 0.0, 3.19, F); rect(8.0, 8.76, 3.4, 3.42, 'glassr')
text(6.35, 3.0, '台盆', 'tiny'); text(7.6, 2.92, '马桶', 'tiny'); text(8.38, 3.0, '淋浴', 'tiny')
# ---------- 房间名与面积 ----------
for name, area, x, z in [
    ('洗浴区', '8.6㎡', 1.35, 1.95), ('衣帽间', '8.3㎡', 1.42, 6.3), ('洗衣区', '2.9㎡', 1.4, 8.25),
    ('玄关 · 手办长廊', '6.7㎡', 4.35, 3.85), ('影音区', '12.9㎡', 3.95, 4.6) , ('睡眠区', '7.9㎡', 7.2, 7.75),
    ('实验工作区', '5.8㎡', 3.75, 8.42), ('手办展示角', '4.9㎡', 7.3, 8.6), ('客卫', '5.1㎡', 7.3, 3.85),
    ('电梯厅', '3.5㎡', 4.2, 1.25), ('电梯', '', 2.5, 1.3)]:
    text(x, z, name, 'room'); 
    if area: text(x, z + 0.26, area, 'area')
# ---------- 尺寸标注 ----------
def dimx(xs, z, off):
    zz = z + off
    line(xs[0], zz, xs[-1], zz, 'dim')
    for x in xs: line(x, zz - 0.09, x, zz + 0.09, 'tick'); line(x, z, x, zz + (0.12 if off > 0 else -0.12), 'ext')
    for a, b in zip(xs, xs[1:]): text((a + b) / 2, zz - 0.08 if off < 0 else zz - 0.08, f'{round((b-a)*1000)}', 'dimt')
def dimz(zs, x, off):
    xx = x + off
    line(xx, zs[0], xx, zs[-1], 'dim')
    for z in zs: line(xx - 0.09, z, xx + 0.09, z, 'tick'); line(x, z, xx + (0.12 if off > 0 else -0.12), z, 'ext')
    for a, b in zip(zs, zs[1:]): text(xx - 0.08, (a + b) / 2, f'{round((b-a)*1000)}', 'dimt', 'middle', -90)
dimx([0, 1.6, 3.4, 5.0, 9.0], 0, -0.55); dimx([0, 9.0], 0, -1.05)
dimx([0, 2.6, 5.0, 9.0], 10, 0.6); dimx([0, 9.0], 10, 1.1)
dimz([0, 2.5, 8.5, 10], 0, -0.55); dimz([0, 10], 0, -1.05)
dimz([0, 2.5, 4.5, 10], 9, 0.75); dimz([0, 10], 9, 1.25)
text(4.5, 11.85, '四层平面图　1:100　标高 +10.200　层高 3.2 m', 'title')
text(4.5, 12.2, '单位：mm（标注为轴线 / 外包尺寸）　临街一侧在下　家具为示意尺寸', 'note')
css = '''
text{font-family:"WenQuanYi Zen Hei","Noto Sans SC",sans-serif;fill:#1c2125}
.ext{fill:#2b2f33}.int{fill:#6b7176}.col{fill:#111}
.winbg{fill:#fff}.win{stroke:#3a6ea5;stroke-width:1.2}
.leaf{stroke:#1c2125;stroke-width:1.6}.swing{fill:none;stroke:#1c2125;stroke-width:0.8;stroke-dasharray:3 2}
.slide{stroke:#fff;stroke-width:5}
.stair{fill:#f1efe9;stroke:#9a9e9f;stroke-width:0.8}.tread{stroke:#b5b9ba;stroke-width:0.8}
.arrow{stroke:#1c2125;stroke-width:1;marker-end:url(#ar)}
.lift{fill:none;stroke:#9a9e9f;stroke-width:0.8}.thin{stroke:#b5b9ba;stroke-width:0.6}
.furn{fill:#fff;stroke:#5a646b;stroke-width:0.9}.wood{fill:#efe3d3;stroke:#8a6a4c;stroke-width:0.9}
.show{fill:#e3eef4;stroke:#3a6ea5;stroke-width:0.9}.rug{fill:#f6f2ec;stroke:#c9bfb0;stroke-width:0.8;stroke-dasharray:5 3}
.pillow{fill:#f5f5f5;stroke:#9aa3a8;stroke-width:0.6}.wet{fill:#e8eef1;stroke:none}
.glass,.glassr{stroke:#3a6ea5;stroke-width:1.4;fill:#3a6ea5}.tv{stroke:#1c2125;stroke-width:3}
.spot{fill:rgba(185,85,47,.12);stroke:#b9552f;stroke-width:1;stroke-dasharray:4 3}
.plant{fill:#cfe0c3;stroke:#6f8f5b}
.dash{stroke:#8a8f93;stroke-width:0.8;stroke-dasharray:4 3}
.dim{stroke:#b9552f;stroke-width:0.8}.tick{stroke:#b9552f;stroke-width:1.4}.ext{stroke:#b9552f;stroke-width:0.4}
rect.ext{stroke:none}
.dimt{font-size:11px;fill:#b9552f}
.room{font-size:13px;font-weight:700}.area{font-size:11px;fill:#5a646b}
.small{font-size:11px;fill:#5a646b}.tiny{font-size:9.5px;fill:#5a646b}
.title{font-size:16px;font-weight:700}.note{font-size:11px;fill:#5a646b}
'''
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1c2125"/></marker></defs>
<style>{css}</style><rect width="100%" height="100%" fill="#ffffff"/>
{chr(10).join(out)}
</svg>'''
import sys
open(sys.argv[1], 'w').write(svg)
