function digest(trunks) {
    for (let i = 0; i < trunks.length; i++) {
        let trunk = trunks[i];
        trunk.en_trunk = trunk.en_trunk.trim();
        trunk.cn_trunk = trunk.cn_trunk.trim();
        trunk.x_trunk = '';
        if (trunk.en_trunk.length > 0 && trunk.cn_trunk.length > 0) {
            trunk.en_trunk_digest = text_digest(trunk.en_trunk, 50);
            trunk.cn_trunk_digest = text_digest(trunk.cn_trunk, 50);
            continue;
        } else if (trunk.en_trunk.length === 0 && trunk.cn_trunk.length === 0) {
            trunk.en_trunk_digest = '';
            trunk.cn_trunk_digest = '';
            continue
        } else if (trunk.cn_trunk.length === 0 && trunk.en_trunk.length > 0) {
            trunk.x_trunk = trunk.en_trunk;
        } else if (trunk.en_trunk.length === 0 && trunk.cn_trunk.length > 0) {
            trunk.x_trunk = trunk.cn_trunk;
        }
        trunk.x_trunk_digest = text_digest(trunk.x_trunk, 100);
    }
}

function text_digest(text, n) {
    if (text.length <= n) {
        return text;
    } else {
        return text.substring(0, n - 3) + '...';
    }
}