# カット3を2本に分けて作る指示文

Space: `mcp-tools/wan-2-2-first-last-frame`。シード1177087716(固定)。
禁止の指示文は、既定の中国語の文に次の語を足す: 腿、脚、四肢、兔子、身体拉长、跳跃、水壶消失、眼睛变圆、眼睛高光、表情变化、站立、飞起来。
カット10の2回目より「站立(立ち上がる)」「飞起来(飛び上がる)」を足した。wan-cut03-1 で縦に立ち、跳んで見えたため。

## A. 始点 → 中間(2秒)

- 始点: `generated/py-cut03-start.png`
- 終点: `generated/py-cut03-mid.png`

```
Flat 2D cartoon animation at evening. A small pale slug with no legs is at the foot of the flat stone. It first lowers its two antennae once, then slowly creeps up the front face of the stone like a slug, keeping its low rounded bean-shaped body pressed against the surface, until its front half rests on the top edge. Its round blue canteen stays on its back the whole time, strapped across its body. It keeps facing right. Static camera. Keep the same simple thick black outlines and flat colors as the input images.
```

## B. 中間 → 終点(1秒)

- 始点: `generated/py-cut03-mid.png`
- 終点: #19 の `generated/py-cut03.png`

```
Flat 2D cartoon animation at evening. A small pale slug with no legs has its front half on the top edge of the flat stone. It slowly pulls the rest of its low rounded bean-shaped body up onto the top, gliding like a slug, and settles. Its round blue canteen stays on its back the whole time, strapped across its body. It keeps facing right. Static camera. Keep the same simple thick black outlines and flat colors as the input images.
```
