import { useCallback, useEffect, useMemo, useState } from 'react'

const TOKEN_KEY = 'auth_token'
const LOGIN_PATH = '/login'
const WELCOME_PATH = '/welcome'

const hasTokenInSession = () => Boolean(sessionStorage.getItem(TOKEN_KEY))

const getInitialPath = () => {
  if (window.location.pathname === WELCOME_PATH && hasTokenInSession()) {
    return WELCOME_PATH
  }
  return LOGIN_PATH
}

function App() {
  const [path, setPath] = useState(getInitialPath)
  const [token, setToken] = useState(() => sessionStorage.getItem(TOKEN_KEY) ?? '')
  const [username, setUsername] = useState('')
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const saveToken = useCallback((nextToken) => {
    setToken(nextToken)
    if (nextToken) {
      sessionStorage.setItem(TOKEN_KEY, nextToken)
      return
    }
    sessionStorage.removeItem(TOKEN_KEY)
  }, [])

  const goTo = useCallback((nextPath, replace = false) => {
    const method = replace ? 'replaceState' : 'pushState'
    window.history[method]({}, '', nextPath)
    setPath(nextPath)
  }, [])

  useEffect(() => {
    const onPopState = () => {
      setPath(getInitialPath())
    }

    window.addEventListener('popstate', onPopState)
    return () => {
      window.removeEventListener('popstate', onPopState)
    }
  }, [])

  useEffect(() => {
    if (path === LOGIN_PATH && window.location.pathname !== LOGIN_PATH) {
      window.history.replaceState({}, '', LOGIN_PATH)
    }
  }, [path])

  useEffect(() => {
    if (path !== WELCOME_PATH || !token) {
      return
    }

    let isCancelled = false

    const loadCurrentUser = async () => {
      try {
        const response = await fetch('/me', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!response.ok) {
          throw new Error('Tu sesión ya no es válida. Inicia sesión nuevamente.')
        }

        const data = await response.json()
        if (!isCancelled) {
          setUsername(data.username)
          setError('')
        }
      } catch (loadError) {
        if (!isCancelled) {
          saveToken('')
          setUsername('')
          setError(loadError.message)
          goTo(LOGIN_PATH, true)
        }
      }
    }

    loadCurrentUser()

    return () => {
      isCancelled = true
    }
  }, [goTo, path, saveToken, token])

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      const payload = new URLSearchParams({
        username: form.username,
        password: form.password,
      })

      const response = await fetch('/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: payload,
      })

      if (!response.ok) {
        throw new Error('Credenciales inválidas. Verifica usuario y contraseña.')
      }

      const data = await response.json()
      saveToken(data.access_token)
      setUsername(form.username)
      goTo(WELCOME_PATH)
    } catch (submitError) {
      saveToken('')
      setUsername('')
      setError(submitError.message)
    } finally {
      setLoading(false)
    }
  }

  const welcomeMessage = useMemo(() => {
    if (!username) {
      return 'Bienvenido'
    }
    return `Bienvenido, ${username}`
  }, [username])

  const logout = () => {
    saveToken('')
    setUsername('')
    setError('')
    goTo(LOGIN_PATH, true)
  }

  return (
    <main className="page-shell">
      <section className="glass-frame">
        <article className="glass-panel">
          <header className="panel-header">
            <p className="kicker">Compliance Platform</p>
            <h1>{path === LOGIN_PATH ? 'Iniciar sesión' : welcomeMessage}</h1>
            <p className="panel-description">
              Dashboard section with clear information density, modular panels and interface rhythm.
            </p>
          </header>

          {error && <p className="message error">{error}</p>}

          {path === LOGIN_PATH ? (
            <form className="auth-form" onSubmit={handleSubmit}>
              <label>
                Usuario
                <input
                  type="text"
                  value={form.username}
                  onChange={(event) => setForm({ ...form, username: event.target.value })}
                  required
                />
              </label>
              <label>
                Contraseña
                <input
                  type="password"
                  value={form.password}
                  onChange={(event) => setForm({ ...form, password: event.target.value })}
                  required
                />
              </label>
              <button type="submit" disabled={loading}>
                {loading ? 'Ingresando...' : 'Entrar'}
              </button>
            </form>
          ) : (
            <div className="welcome-view">
              <p className="message">La sesión está activa y protegida con token en sessionStorage.</p>
              <button type="button" onClick={logout}>
                Cerrar sesión
              </button>
            </div>
          )}
        </article>
      </section>
    </main>
  )
}

export default App
