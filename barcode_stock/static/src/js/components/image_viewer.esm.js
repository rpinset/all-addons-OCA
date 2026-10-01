import {Component, onWillUpdateProps, useState} from "@odoo/owl";

export class ImageViewer extends Component {
    setup() {
        this.state = useState({
            currentIndex: this.props.initialIndex || 0,
        });
        this.touchStartX = 0;

        onWillUpdateProps((nextProps) => {
            if (this.state.currentIndex >= nextProps.images.length) {
                this.state.currentIndex = Math.max(0, nextProps.images.length - 1);
            }
        });
    }

    get currentImageId() {
        return this.props.images[this.state.currentIndex];
    }

    get currentImageSrc() {
        return this.currentImageId ? `/web/image/${this.currentImageId}` : "";
    }

    nextImage() {
        const total = this.props.images.length;
        this.state.currentIndex = (this.state.currentIndex + 1) % total;
    }

    prevImage() {
        const total = this.props.images.length;
        this.state.currentIndex = (this.state.currentIndex - 1 + total) % total;
    }

    deleteImage() {
        const imgId = this.currentImageId;
        if (imgId !== undefined) {
            this.props.onDeleteImage(imgId);
        }
    }

    onTouchStart(ev) {
        this.touchStartX = ev.changedTouches[0].screenX;
    }

    onTouchEnd(ev) {
        const touchEndX = ev.changedTouches[0].screenX;
        const diff = touchEndX - this.touchStartX;
        if (Math.abs(diff) < 50) {
            return;
        }
        if (diff < 0) {
            this.nextImage();
        } else {
            this.prevImage();
        }
    }
}

ImageViewer.template = "barcode_scanner.ImageViewer";
ImageViewer.props = {
    images: {type: Array, element: Number},
    initialIndex: {type: Number, optional: true},
    onClose: Function,
    onDeleteImage: Function,
};
