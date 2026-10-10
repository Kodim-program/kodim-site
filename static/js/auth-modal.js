(function () {
    var modal = document.getElementById('kdAuth');
    if (!modal) return;

    var tabs = modal.querySelectorAll('.kd-auth__tab');
    var panes = modal.querySelectorAll('.kd-auth__pane');

    function clearErrors() {
        modal.querySelectorAll('.kd-auth__error').forEach(function (el) { el.remove(); });
    }

    function show(mode) {
        tabs.forEach(function (t) { t.classList.toggle('is-active', t.dataset.authTab === mode); });
        panes.forEach(function (p) { p.classList.toggle('is-active', p.dataset.authPane === mode); });
        clearErrors();
    }

    function open(mode) {
        show(mode || 'login');
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('kd-auth-lock');
        var input = modal.querySelector('.kd-auth__pane.is-active input[type="text"]');
        if (input) setTimeout(function () { input.focus(); }, 50);
    }

    function close() {
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('kd-auth-lock');
    }

    function showErrors(form, errors) {
        clearErrors();
        var box = document.createElement('div');
        box.className = 'kd-auth__error';
        errors.forEach(function (text) {
            var line = document.createElement('div');
            line.textContent = text;
            box.appendChild(line);
        });
        form.insertBefore(box, form.firstElementChild.nextElementSibling);
    }

    // Після успішного входу: оновлюємо сторінку «на місці»
    function onAuthSuccess(data) {
        // 1) нові CSRF-токени у всіх формах на сторінці
        if (data.csrf) {
            document.querySelectorAll('input[name="csrfmiddlewaretoken"]').forEach(function (i) {
                i.value = data.csrf;
            });
        }
        // 2) кнопка «Авторизація» → «Профіль»
        document.querySelectorAll('[data-auth-slot]').forEach(function (slot) {
            slot.innerHTML =
                '<a href="' + data.profile_url + '"><button type="button" class="btn">' +
                '<i class="animation"></i>Профіль<i class="animation"></i></button></a>';
        });
        // 3) очищаємо форми (щоб пароль не залишався в DOM) і закриваємо вікно
        panes.forEach(function (f) { f.reset(); });
        setTimeout(close, 500);
        // 4) подія для інших скриптів на сторінці
        document.dispatchEvent(new CustomEvent('kdauth:login', { detail: data }));
    }

    // capture-фаза: спрацьовує раніше за скрипти теми
    document.addEventListener('click', function (e) {
        var opener = e.target.closest('[data-auth-open]');
        if (opener) {
            e.preventDefault();
            e.stopPropagation();
            open(opener.dataset.authOpen);
            return;
        }
        if (e.target.closest('[data-auth-close]')) { close(); return; }

        var tab = e.target.closest('[data-auth-tab]');
        if (tab && modal.contains(tab)) { e.preventDefault(); show(tab.dataset.authTab); return; }

        var eye = e.target.closest('[data-auth-eye]');
        if (eye) {
            var input = eye.parentNode.querySelector('input');
            var hidden = input.type === 'password';
            input.type = hidden ? 'text' : 'password';
            eye.firstElementChild.className = hidden ? 'fa fa-eye-slash' : 'fa fa-eye';
        }
    }, true);

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) close();
    });

    // AJAX-відправка форм
    panes.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var btn = form.querySelector('.kd-auth__submit');
            var label = btn.textContent;
            btn.disabled = true;
            btn.textContent = 'Зачекайте…';

            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                credentials: 'same-origin',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(function (r) {
                    var type = r.headers.get('content-type') || '';
                    if (type.indexOf('application/json') === -1) throw new Error('NOT_JSON_' + r.status);
                    return r.json().then(function (data) { return { ok: r.ok, data: data }; });
                })
                .then(function (res) {
                    if (res.ok && res.data.ok) {
                        btn.textContent = 'Успішно ✓';
                        // на окремих сторінках /users/login/ та /users/registration/ — перехід
                        if (modal.dataset.open) {
                            window.location.href = res.data.redirect || '/';
                            return;
                        }
                        onAuthSuccess(res.data);
                        btn.disabled = false;
                        btn.textContent = label;
                    } else {
                        showErrors(form, res.data.errors || ['Сталася помилка. Спробуйте ще раз.']);
                        btn.disabled = false;
                        btn.textContent = label;
                    }
                })
                .catch(function (err) {
                    var msg = String(err.message || '');
                    if (msg.indexOf('NOT_JSON_') === 0) {
                        var code = msg.replace('NOT_JSON_', '');
                        msg = code === '403'
                            ? 'Помилка безпеки (CSRF). Оновіть сторінку й спробуйте ще раз.'
                            : 'Сервер повернув неочікувану відповідь (' + code + '). Оновіть сторінку.';
                    } else {
                        msg = 'Немає зв’язку із сервером. Перевірте інтернет.';
                    }
                    showErrors(form, [msg]);
                    btn.disabled = false;
                    btn.textContent = label;
                });
        });
    });

    var auto = modal.dataset.open;
    if (auto) open(auto === 'register' ? 'register' : 'login');
    else show('login');

    window.kdAuth = { open: open, close: close };
})();