import os

path = r'd:/Projects/Hyperlocal-Inventory/Frontends/market-place/src/features/purchase/pages/PurchaseHistory.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """        onConfirm={async () => {
          if (!poToDelete) return;
          try {
            const activeShopId = localStorage.getItem("shop_id") || SHOP_ID;
            await purchase.deletePurchase(activeShopId, poToDelete.id);
            showToast("Draft purchase deleted successfully.", "success");
            setPoToDelete(null);
            if (onRefresh) onRefresh();
            else window.location.reload();
          } catch (err: any) {
            console.error("Failed to delete purchase:", err);
            const msg = err?.message || err?.detail?.description || err?.response?.data?.detail?.description || err?.response?.data?.detail?.msg || err?.response?.data?.detail || "Failed to delete draft purchase.";
            showToast(typeof msg === 'string' ? msg : "Failed to delete draft purchase.", "error");
          }
        }}"""

replacement = """        onConfirm={async () => {
          if (!poToDelete) return;
          try {
            const activeShopId = localStorage.getItem("shop_id") || SHOP_ID;
            const targetId = poToDelete.id || (poToDelete as any).purchase_id || poToDelete.systemId;
            await purchase.deletePurchase(activeShopId, targetId);
            showToast("Draft purchase deleted successfully.", "success");
            const deletedId = poToDelete.id;
            setPoToDelete(null);
            setData((prev) => prev.filter((item) => item.id !== deletedId));
            if (onRefresh) onRefresh();
          } catch (err: any) {
            console.error("Failed to delete purchase:", err);
            const msg = err?.message || err?.detail?.description || err?.response?.data?.detail?.description || err?.response?.data?.detail?.msg || err?.response?.data?.detail || "Failed to delete draft purchase.";
            showToast(typeof msg === 'string' ? msg : "Failed to delete draft purchase.", "error");
          }
        }}"""

if target in content:
    content = content.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS")
else:
    print("TARGET NOT FOUND")
