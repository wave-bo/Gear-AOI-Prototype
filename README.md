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

## 📊 检测结果 (Results)
| 状态 (Status) | 说明 (Description) | 判定 (Verdict) |
| :--- | :--- | :--- |
| **QUALIFIED** | 形状相似度与面积偏差在阈值内 | PASS (合格) |
| **DEFECTIVE** | 存在几何缺损（如缺齿）或尺寸超差 | REJECT (不合格) |