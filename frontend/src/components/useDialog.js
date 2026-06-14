import { createApp, h } from 'vue';
import Dialog from './Dialog.vue';

function mountDialog(props) {
  return new Promise((resolve) => {
    const container = document.createElement('div');
    document.body.appendChild(container);

    const app = createApp({
      render() {
        return h(Dialog, {
          ...props,
          onResolve: (result) => {
            resolve(result);
            app.unmount();
            container.remove();
          }
        });
      }
    });

    app.mount(container);
  });
}

export function useDialog() {
  return {
    alert(message) {
      return mountDialog({
        type: 'alert',
        message
      });
    },

    confirm(message) {
      return mountDialog({
        type: 'confirm',
        message
      });
    },

    input(message, elements = []) {
      return mountDialog({
        type: 'input',
        message,
        elements
      });
    }
  };
}
