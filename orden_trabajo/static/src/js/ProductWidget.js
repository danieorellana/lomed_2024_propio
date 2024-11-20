/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class ProductWidget extends Component {
    static template = "orden_trabajo.products";

    setup() {
        this.state = useState({ productos: [] });
    }

   
}