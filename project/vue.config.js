module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'https://www.supermapol.com/',
                ws: true,
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    },
}
