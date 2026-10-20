import {imageUrl} from "@web/core/utils/urls";

/**
 * URL of a record's image, or false when it has none.
 *
 * Odoo's own image route, rather than a hand-built "data:image/png;base64,"
 * URI: the field holds whatever format was uploaded -- jpg, gif, webp, svg --
 * and a browser will not render an svg announced as a png, which is what left
 * broken avatars in these lists. The route sends the right mimetype and serves
 * a placeholder when the record has no image or it cannot be decoded.
 *
 * Read the image field with `{context: {bin_size: true}}` and alongside
 * `write_date`: the field then reads back as a short size string, which still
 * says whether an image exists while keeping every full image off the PDA's
 * connection, and `write_date` versions the URL so a changed image is not
 * served from cache.
 */
export function recordImageUrl(model, record, field = "image_128") {
    return record[field]
        ? imageUrl(model, record.id, field, {unique: record.write_date})
        : false;
}
