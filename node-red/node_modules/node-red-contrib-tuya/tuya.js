const TuyaDevice = require('tuyapi');

module.exports = RED => {
    function TuyaNode(config) {
        RED.nodes.createNode(this, config);
        const node = this;

        let device = new TuyaDevice({
            id: config.uuid,
            key: this.credentials.key,
            ip: config.ip || null
        });

        this.on('input', function(msg) {
          device.set({set: msg.payload})
            .then(() => {})
            .catch(e => this.error(e));
        });

        const interval = setInterval(() => {
          device.get().then(status => {
            node.send({
              payload: status
            })
          });
        }, 5000);

        this.on('close', function() {
          clearInterval(interval);
      });
    }

    RED.nodes.registerType('tuya', TuyaNode, {
        credentials: {
          key: { type: "text" }        
        }
    });

}