/**
 * @license
 * Copyright (c) 2019 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
import { LitElement, PropertyValues } from 'lit-element';
import 'mil-pulse-spinner';
export declare class FaceImage extends LitElement {
    image: string;
    box: {
        name?: string;
        top: number;
        right: number;
        bottom: number;
        left: number;
    }[];
    static styles: import("lit-element").CSSResult;
    ratioX: number;
    ratioY: number;
    render(): import("lit-element").TemplateResult;
    updated(_changedProperties: PropertyValues): void;
    imageCmp: HTMLImageElement;
    private crop;
    getData(): HTMLCanvasElement;
    extractFaces(): {
        name: string;
        data: HTMLCanvasElement;
    }[];
}
declare global {
    interface HTMLElementTagNameMap {
        'face-image': FaceImage;
    }
}
//# sourceMappingURL=Face-Image.d.ts.map