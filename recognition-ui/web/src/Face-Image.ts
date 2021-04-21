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

import {LitElement, html, customElement, property, css, internalProperty, PropertyValues, query} from 'lit-element';
import 'mil-pulse-spinner';
 
 @customElement('face-image')
 export class FaceImage extends LitElement {


  @property({type: String})
  image: string;

  @property({type: Array})
  box: {name?:string; top:number; right:number; bottom:number; left:number}[];

  static styles = css`
    :host {
      display: block;
      position: relative;
    }
 
    :host([processing]) {
      filter: brightness(0.5);
   }

    .rect {
      position: absolute;
      border: 1px solid red;
    }

    .face:hover .label {
      display: none;
    }

    .face:not(:hover) .editor {
      display: none;
    }

    .label {
      background-color: lightgray;
    }
    img {
      width: 100%;
    }

    input {
      width: 100%;
    }

    .delete {
      position: absolute;
      width: 25px;
      height: 25px;
      background: black;
      cursor: pointer;
    }

    mil-pulse-spinner {
      --width: 100px;
      --height: 100px;
      position: absolute;
      width: 100%;
      height: 100%;
      margin-top: calc(50% - 50px);
    }

    :host(:not([processing])) mil-pulse-spinner {
      display: none;
    }
  `;


@internalProperty()
ratioX = 0; 

@internalProperty()
ratioY = 0;

  render() {
    const deleteButton = html`<img class="delete" style="top: 0px; right: 0px;" src="delete.png" @click="${ () => this.remove()}"/>`;
    const processing = html`<mil-pulse-spinner></mil-pulse-spinner>`;

    if ( this.box === undefined ) return html`
        ${processing}<img id="image" src="${this.image}"/>${deleteButton}`;


    return html`${processing}<img id="image" src="${this.image}"/>
    ${deleteButton}
    ${this.box.map( (box,index) => html`
      <div class="face">
        <img class="delete" src="delete" style="left:${this.ratioX * box.right - 12.5}px; top:${this.ratioY * box.top - 12.5}px" @click="${ () => { this.box.splice(index, 1); this.requestUpdate()}}"/>
        <div class="rect" style="left:${this.ratioX * box.left}px; top:${this.ratioY * box.top}px; width:${this.ratioX * (box.right - box.left)}px; height:${this.ratioY * (box.bottom - box.top)}px"></div>
        <div class="rect labelHolder" class="rect" style="left:${this.ratioX * box.left}px; top:${this.ratioY * box.bottom}px;width:${this.ratioX * (box.right - box.left)}px;">
          <div class="label">${box.name||""}</div>
          <input class="editor" type="text" @change="${(e) => {box.name = e.target.value; this.requestUpdate()}}" value="${box.name||""}">
        </div>
      </div>
    `)}`;
  }

  updated(_changedProperties: PropertyValues) {
    super.updated(_changedProperties);
    const img = this.shadowRoot.querySelector("img");
    const style = window.getComputedStyle(img);

    this.ratioX = parseFloat(style.width) / img.naturalWidth;
    this.ratioY = parseFloat(style.height) / img.naturalHeight;

  }



  @query("#image")
  imageCmp: HTMLImageElement;

  private crop(offsetX: number, offsetY: number, width: number, height: number) {
    // create an in-memory canvas
    var buffer = document.createElement("canvas");
    var b_ctx = buffer.getContext('2d');
    // set its width/height to the required ones
    buffer.width = width;
    buffer.height = height;
    // draw the main canvas on our buffer one
    // drawImage(source, source_X, source_Y, source_Width, source_Height, 
    //  dest_X, dest_Y, dest_Width, dest_Height)
    b_ctx.drawImage(this.imageCmp, offsetX, offsetY, width, height,
                    0, 0, buffer.width, buffer.height);
    // now call the callback with the dataURL of our buffer canvas
    return buffer;
  };

  getData() {
    const img = this.shadowRoot.querySelector("img");
    return this.crop(0,0,img.naturalWidth, img.naturalHeight);
  }

  extractFaces() {
    return this.box.map( box => { 
      //let buff;
      //let cb = function( data ) { buff = data };
      return {
      name: box.name,
      data: this.crop(box.left,box.top, box.right - box.left, box.bottom - box.top)
    }});
  }
 }
 
 
 
 
 declare global {
   interface HTMLElementTagNameMap {
     'face-image': FaceImage;
   }
 }
 
 