import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 混淆矩陣資料
cm = np.array([[216, 1509],
               [96, 2005]])

# 根據混淆矩陣反推 y_true 和 y_pred
y_true = ([0] * (cm[0][0] + cm[0][1])) + ([1] * (cm[1][0] + cm[1][1]))
y_pred = ([0] * cm[0][0] + [1] * cm[0][1]) + ([0] * cm[1][0] + [1] * cm[1][1])

# 計算指標
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# 建立數據表格
metrics_data = [
    ["Accuracy", f"{accuracy:.4f}"],
    ["Precision", f"{precision:.4f}"],
    ["Recall", f"{recall:.4f}"],
    ["F1-score", f"{f1:.4f}"]
]

# 畫 subplot（1 行 2 欄）
fig, axs = plt.subplots(1, 2, figsize=(11, 5))

# 左邊：confusion matrix
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axs[0])
axs[0].set_title('Confusion Matrix')
axs[0].set_xlabel('Predicted')
axs[0].set_ylabel('Actual')

# 右邊：指標表格
axs[1].axis('off')  # 不顯示坐標軸
table = axs[1].table(cellText=metrics_data,
                     cellLoc='center',
                     loc='center')
table.scale(1, 3)  # 放大表格
table.auto_set_font_size(False)
table.set_fontsize(20)
axs[1].set_title('Classification Report', fontweight='bold')

plt.tight_layout()
# plt.show()

plt.savefig("C:\\Users\\照元喔\\OneDrive\\圖片\\MLRUS.png")