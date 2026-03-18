# JF-AOI: Industrial Gear Inspection System 
### 基于计算机视觉的工业齿轮自动光学检测系统 (原型)

---

## 🚀 项目简介 (Project Overview)
本项目是一个专为工业流水线设计的自动光学检测（AOI）系统原型。通过 Python 与 OpenCV，实现了对精密金属零件（齿轮）的快速识别、形状比对及质量筛选。

This project is a prototype of an Automated Optical Inspection (AOI) system designed for industrial production lines. Using Python and OpenCV, it enables rapid identification, shape comparison, and quality screening of precision metal parts (gears).

## 🛠️ 核心技术 (Technical Highlights)
- **Hu-Moments 拓扑匹配**: 采用胡氏矩算法实现 360 度旋转无关的形状识别，确保零件在传送带上任意角度均可精准比对。
- **形态学抗噪处理 (Morphology)**: 针对金属表面斑驳纹理与反光进行了闭合（Closing）算子优化，提升了复杂环境下的稳健性。
- **重心定位算法 (Centroid Localization)**: 基于图像矩（Moments）计算几何重心：
  $$x = \frac{M_{10}}{M_{00}}, \quad y = \frac{M_{01}}{M_{00}}$$
  确保检测标签动态跟随零件，解决了视觉溢出问题。

- **Hu-Moments Topology Matching**: Rotation-invariant shape recognition for 360° detection.
- **Morphological Robustness**: Optimized closing operators for handling specular reflections and mottled textures on metal surfaces.
- **Centroid Localization**: Dynamic label positioning based on geometric moments.

## 📦 快速开始 (Quick Start)
1. **环境准备**: `pip install opencv-python numpy`
2. **准备样本**: 
   - 将“黄金样本”命名为 `gear_golden.jpg` 放入根目录。
   - 将待测样本命名为 `gear_1.jpg`, `gear_2.jpg` 等。
3. **运行检测**: `python main.py`

## 📊 检测结果展示 (Inspection Results Showcase)

本系统采用严格的几何拓扑分析，可有效甄别外观细微差异。

The system utilizes strict geometric topology analysis to effectively identify subtle visual differences.

### 1. 合格样本 (Qualified Sample - PASS)
> 形状极其贴合，几何特征与黄金样本高度一致。

![Qualified Result](screenshots/result_qualified.jpg)

### 2. 不合格样本 (Defective Sample - REJECT)
> 虽然形状大致也是圆形，但由于铁锈纹理和diffuse边界，导致局部拓扑结构（方差）显著不一致，系统果断拦截。

![Defective Result](screenshots/result_defective.jpg)