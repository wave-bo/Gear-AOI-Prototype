import cv2
import numpy as np
import glob
import os

# --- JF-AOI 项目配置参数 ---
# 稍微收紧阈值，防止缺齿零件漏检
GAUSSIAN_K = (5, 5)
MORPH_K = (5, 5)        # 调小一点，线条更贴合
MIN_AREA = 20000        
# 重点：这个值越小越严格，0.05 是个比较稳的精密档位
SHAPE_TOLERANCE = 0.05  
AREA_TOLERANCE = 0.12   

def get_gear_features(img):
    """ 提取齿轮几何特征的核心函数 """
    # 基础预处理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, GAUSSIAN_K, 0)
    
    # 提取边缘 - 阈值根据现场光照可能需要微调
    edges = cv2.Canny(blur, 40, 100)

    # 形态学闭合，连接断裂边缘
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, MORPH_K)
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # 获取外轮廓
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
        
    # 工业逻辑：取面积最大的物体作为目标，过滤细碎杂质
    target = max(contours, key=cv2.contourArea)
    return target

def run_inspector():
    # 基准样本路径
    ref_path = "gear_golden.jpg"
    if not os.path.exists(ref_path):
        print(f"Critial Error: 缺失基准图 {ref_path}")
        return

    # 初始化基准特征
    ref_img = cv2.imread(ref_path)
    ref_cnt = get_gear_features(ref_img)
    if ref_cnt is None:
        print("Error: 基准图特征提取失败，请检查图片质量")
        return
    
    ref_area = cv2.contourArea(ref_cnt)
    print(f"System Ready. 基准面积: {int(ref_area)}")

    # 批量扫描目录下的 gear_*.jpg
    test_queue = glob.glob("gear_*.jpg")
    
    for path in test_queue:
        if "golden" in path: continue  # 跳过基准图自身

        frame = cv2.imread(path)
        if frame is None: continue

        display = frame.copy()
        curr_cnt = get_gear_features(frame)

        if curr_cnt is not None:
            # 1. 形状比对 (Hu Moments)
            # 原理：计算两个几何体之间的拓扑距离
            s_diff = cv2.matchShapes(ref_cnt, curr_cnt, cv2.CONTOURS_MATCH_I1, 0.0)
            
            # 2. 面积偏差比对
            curr_area = cv2.contourArea(curr_cnt)
            a_diff = abs(ref_area - curr_area) / ref_area

            # 计算重心 (Centroid) 用于绘制标签
            M = cv2.moments(curr_cnt)
            if M["m00"] != 0:
                cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            else:
                cX, cY = curr_cnt[0][0]

            # 综合判定逻辑
            passed = (s_diff < SHAPE_TOLERANCE) and (a_diff < AREA_TOLERANCE)
            
            res_color = (0, 255, 0) if passed else (0, 0, 255)
            msg = "QUALIFIED" if passed else "DEFECTIVE"

            # 绘图反馈
            cv2.drawContours(display, [curr_cnt], -1, res_color, 2)
            
            # 绘制中心标签
            tag = f"Area:{int(curr_area)}"
            cv2.putText(display, tag, (cX-50, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 3)
            cv2.putText(display, tag, (cX-50, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            
            # 结果 banner
            cv2.putText(display, f"[{msg}]", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, res_color, 3)
            
            print(f"Checked: {path} | Diff: {s_diff:.4f} | Result: {msg}")
        
        else:
            print(f"Skip: {path} - 未能定位零件")

        # 结果展示
        h, w = display.shape[:2]
        cv2.imshow("JF-AOI Inspection Console", cv2.resize(display, (800, int(h * 800 / w))))
        
        if cv2.waitKey(0) == ord('q'): break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_inspector()