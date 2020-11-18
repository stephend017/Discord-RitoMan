module.exports = {
  apps: [{
    name: "ritoman",
    cmd: "discord_ritoman/__main__.py",
    interpreter: "python3",
    env: {
      DB_PASS: process.env.DB_PASS,
      RIOT_TOKEN: process.env.RIOT_TOKEN,
      DISCORD_BOT: process.env.DISCORD_BOT
    }
  }],

  deploy : {
    production : {
      user : 'root',
      host: '67.207.83.34',
      ref  : 'origin/main',
      repo: 'https://github.com/stephend017/discord_ritoman.git',
      path : '/root/discord_ritoman',
      'post-deploy' : 'python3.8 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pip install . && pm2 reload ecosystem.config.js --env production',
      env: {
        DB_PASS: process.env.DB_PASS,
        RIOT_TOKEN: process.env.RIOT_TOKEN,
        DISCORD_BOT: process.env.DISCORD_BOT
      }
    }
  }
};
