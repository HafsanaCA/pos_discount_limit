/** @odoo-module **/
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PosStore.prototype, {
    async pay() {
        const pos_session = this.config.current_session_id;
        const order = this.get_order();
        const allow_discount_control = pos_session?.allow_discount_control ?? false;
        const max_allowed_discount = pos_session?.max_allowed_discount ?? 0;

        if (allow_discount_control) {
            let totalLineDiscount = 0;
            let totalGlobalDiscount = 0;
            const discountProductId = this.config.discount_product_id?.id;

            order.get_orderlines().forEach(line => {
                if (line.product_id?.id === discountProductId) {
                    totalGlobalDiscount += Math.abs(line.get_price_with_tax());
                } else {
                    const unitPrice = line.get_unit_price();
                    const discount = line.get_discount();
                    const quantity = line.get_quantity();
                    totalLineDiscount += (unitPrice * discount / 100) * quantity;
                }
            });
            const totalDiscount = totalLineDiscount + totalGlobalDiscount;

            if (totalDiscount > max_allowed_discount || max_allowed_discount <= 0) {
                await this.env.services.dialog.add(AlertDialog, {
                    title: _t("Validation Error"),
                    body: _t("Maximum discount amount allowed for this session is exceeded."),
                });
                return;
            }
            pos_session.max_allowed_discount -= totalDiscount;
        }
        return super.pay();
    }
});
