#!/usr/bin/env python3
"""
🍺 CRAFT V2.0 — Frontend HTML/CSS/JS template
"""

from flask import Blueprint, Response

frontend_bp = Blueprint('frontend', __name__)

MAIN_HTML = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="build" content="20260222-0910">
<title>🍺 CRAFT V2.0</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#1A1209;color:#FFF8E7;font-family:'Helvetica','Helvetica Neue',Arial,sans-serif;min-height:100vh;overflow-x:hidden;position:relative}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:linear-gradient(180deg,#1A1209 0%,#2A1A0A 30%,#1E1308 60%,#0F0A04 100%);z-index:0;pointer-events:none}
/* ✨ БЛЕСТЯЩИЕ ПИВНЫЕ ПУЗЫРЬКИ */
.bubbles{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden}
.bubble{position:absolute;bottom:-30px;border-radius:50%;will-change:transform,opacity;transform:translateZ(0);animation:bubbleRise linear infinite,bubbleSparkle 2s ease-in-out infinite,bubbleWobble 3s ease-in-out infinite;
  background:radial-gradient(circle at 30% 30%,rgba(255,248,200,0.9) 0%,rgba(244,196,48,0.7) 20%,rgba(212,135,28,0.5) 50%,rgba(184,134,11,0.3) 75%,transparent 100%);
  box-shadow:inset 0 0 8px rgba(255,248,231,0.7),0 0 15px rgba(244,196,48,0.5),0 0 30px rgba(212,135,28,0.3),0 0 45px rgba(184,115,51,0.15);
  backdrop-filter:blur(1px)}
.bubble::after{content:'';position:absolute;top:15%;left:20%;width:35%;height:25%;background:radial-gradient(ellipse,rgba(255,255,255,0.8) 0%,transparent 70%);border-radius:50%;transform:rotate(-30deg)}
@keyframes bubbleRise{0%{transform:translateY(0) translateX(0) scale(1);opacity:0}5%{opacity:0.8}50%{transform:translateY(-55vh) translateX(15px) scale(0.85);opacity:0.6}100%{transform:translateY(-115vh) translateX(-10px) scale(0.3);opacity:0}}
@keyframes bubbleSparkle{0%,100%{filter:brightness(1) drop-shadow(0 0 4px rgba(244,196,48,0.4))}25%{filter:brightness(1.4) drop-shadow(0 0 8px rgba(244,196,48,0.7))}50%{filter:brightness(1.6) saturate(1.3) drop-shadow(0 0 12px rgba(255,215,0,0.8))}75%{filter:brightness(1.2) drop-shadow(0 0 6px rgba(212,175,55,0.5))}}
@keyframes bubbleWobble{0%,100%{transform:translateX(0)}33%{transform:translateX(8px)}66%{transform:translateX(-6px)}}
.screen,.overlay,.gate-overlay{position:relative;z-index:1}
.screen{display:none;flex-direction:column;min-height:100vh;width:100%}
.screen.active{display:flex}
/* Header — Барная стойка */
.header{background:linear-gradient(180deg,rgba(35,22,10,.98) 0%,rgba(50,30,12,.95) 100%);padding:22px 16px;text-align:center;border-bottom:2px solid rgba(212,135,28,.4);box-shadow:0 4px 20px rgba(0,0,0,.5);position:relative}
.header::after{content:'';position:absolute;bottom:-2px;left:10%;width:80%;height:2px;background:linear-gradient(90deg,transparent,#F4C430,#D4871C,#F4C430,transparent)}
.uid{font-size:20px;font-weight:700;color:#F4C430;margin-bottom:6px;text-shadow:0 0 10px rgba(244,196,48,.4);letter-spacing:1px;font-family:'Helvetica','Helvetica Neue',Arial,sans-serif}
.balance{font-size:14px;color:#C9A84C;text-shadow:0 0 5px rgba(201,168,76,.3)}
/* Grid */
.main-grid{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:24px 16px;max-width:400px;margin:0 auto;width:100%}
/* Карточки — пивные подставки */
.main-block{background:linear-gradient(145deg,rgba(60,40,15,.95),rgba(40,25,10,.98));border:2px solid rgba(212,135,28,.35);border-radius:18px;padding:24px 16px;text-align:center;cursor:pointer;transition:all .3s;min-height:130px;display:flex;flex-direction:column;justify-content:center;-webkit-tap-highlight-color:transparent;box-shadow:0 4px 15px rgba(0,0,0,.4),inset 0 1px 0 rgba(212,175,55,.15);position:relative;overflow:hidden}
.main-block::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(244,196,48,.5),transparent)}
.main-block::after{content:'';position:absolute;bottom:0;left:15%;right:15%;height:1px;background:linear-gradient(90deg,transparent,rgba(184,115,51,.4),transparent)}
.main-block:active{transform:scale(.95);box-shadow:0 2px 8px rgba(0,0,0,.6)}
.main-block:hover{border-color:rgba(244,196,48,.6);box-shadow:0 6px 25px rgba(212,135,28,.25),inset 0 1px 0 rgba(244,196,48,.3);transform:translateY(-2px)}
.block-icon{font-size:40px;margin-bottom:10px;display:inline-block}
.block-title{font-size:15px;font-weight:700;color:#F4C430;letter-spacing:.5px;text-shadow:0 0 8px rgba(244,196,48,.3)}
.sos-block{background:linear-gradient(145deg,rgba(80,20,15,.9),rgba(50,15,10,.95))!important;border-color:rgba(198,40,40,.5)!important;box-shadow:0 4px 15px rgba(198,40,40,.2),inset 0 1px 0 rgba(255,100,80,.1)!important}
.sos-block .block-icon{animation:sosPulse 1.5s ease-in-out infinite}
.sos-block:hover{border-color:rgba(229,57,53,.7)!important;box-shadow:0 6px 25px rgba(198,40,40,.35)!important}
/* Footer — нижняя барная полка */
.footer{display:flex;justify-content:space-between;padding:16px;background:linear-gradient(180deg,rgba(35,22,10,.95),rgba(25,15,8,.98));border-top:2px solid rgba(212,135,28,.3);position:relative}
.footer::before{content:'';position:absolute;top:-2px;left:10%;width:80%;height:2px;background:linear-gradient(90deg,transparent,rgba(244,196,48,.4),transparent)}
.footer-btn{padding:10px 18px;background:linear-gradient(135deg,rgba(212,135,28,.15),rgba(184,115,51,.2));border:1px solid rgba(212,135,28,.4);border-radius:10px;color:#F4C430;text-decoration:none;font-size:12px;font-weight:600;cursor:pointer;transition:all .2s;letter-spacing:.3px}
.footer-btn:active{background:linear-gradient(135deg,rgba(212,135,28,.35),rgba(184,115,51,.4));transform:scale(.95)}
/* Animations */
@keyframes iconFloat{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-5px) scale(1.05)}}
@keyframes sosPulse{0%,100%{transform:scale(1);opacity:1;filter:drop-shadow(0 0 4px rgba(198,40,40,.5))}50%{transform:scale(1.2);opacity:.85;filter:drop-shadow(0 0 15px rgba(229,57,53,.8))}}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes beerGlow{0%,100%{filter:drop-shadow(0 0 5px rgba(244,196,48,.3))}50%{filter:drop-shadow(0 0 15px rgba(244,196,48,.7)) drop-shadow(0 0 25px rgba(212,175,55,.3))}}
@keyframes beerWiggle{0%,100%{transform:rotate(0deg) scale(1)}20%{transform:rotate(-12deg) scale(1.15)}40%{transform:rotate(8deg) scale(1.2)}60%{transform:rotate(-5deg) scale(1.1)}80%{transform:rotate(3deg) scale(1.05)}}
@keyframes goldShimmer{0%{background-position:200% center}100%{background-position:-200% center}}
.main-block:hover .block-icon,.main-block:active .block-icon{animation:beerWiggle .6s ease-in-out}
.block-icon{animation:iconFloat 3s ease-in-out infinite,beerGlow 2.5s ease-in-out infinite}
.fade-in{animation:fadeIn .3s ease}
/* Overlay screens */
.overlay{position:fixed;top:0;left:0;width:100%;height:100%;z-index:100;display:none;flex-direction:column}
.overlay.active{display:flex}
.overlay-bg{background:linear-gradient(180deg,#1A1209 0%,#2A1A0A 40%,#1E1308 100%);min-height:100vh}
/* Sub-header */
.sub-header{background:linear-gradient(180deg,rgba(35,22,10,.98),rgba(45,28,12,.95));padding:16px;display:flex;align-items:center;gap:12px;border-bottom:2px solid rgba(212,135,28,.3);box-shadow:0 3px 15px rgba(0,0,0,.4);position:relative}
.sub-header::after{content:'';position:absolute;bottom:-2px;left:10%;width:80%;height:2px;background:linear-gradient(90deg,transparent,rgba(244,196,48,.4),transparent)}
.back-btn{width:38px;height:38px;border-radius:50%;border:1.5px solid rgba(244,196,48,.5);background:linear-gradient(135deg,rgba(212,135,28,.15),rgba(184,115,51,.1));color:#F4C430;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s}
.back-btn:active{transform:scale(.9);background:rgba(212,135,28,.3)}
.sub-title{font-size:18px;font-weight:700;color:#F4C430;text-shadow:0 0 8px rgba(244,196,48,.3);letter-spacing:.5px}
/* Content */
.content{flex:1;padding:16px;overflow-y:auto;-webkit-overflow-scrolling:touch}
/* Cards — пивные подставки */
.card{background:linear-gradient(145deg,rgba(55,35,12,.95),rgba(35,22,10,.98));border:1.5px solid rgba(212,135,28,.3);border-radius:14px;padding:18px;margin-bottom:14px;box-shadow:0 4px 12px rgba(0,0,0,.3),inset 0 1px 0 rgba(244,196,48,.1);position:relative}
.card::before{content:'';position:absolute;top:0;left:10%;right:10%;height:1px;background:linear-gradient(90deg,transparent,rgba(244,196,48,.3),transparent)}
.card-title{font-size:15px;font-weight:700;color:#F4C430;margin-bottom:8px;text-shadow:0 0 6px rgba(244,196,48,.2)}
.card-text{font-size:13px;color:#C9A84C;line-height:1.6}
.card-value{font-size:22px;font-weight:700;color:#FFF8E7;text-shadow:0 0 8px rgba(255,248,231,.2)}
/* Stat row */
.stat-row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(212,135,28,.1)}
.stat-label{font-size:13px;color:#C9A84C}
.stat-val{font-size:13px;color:#FFF8E7;font-weight:600}
/* Forms */
.form-group{margin-bottom:14px}
.form-label{display:block;font-size:13px;color:#C9A84C;margin-bottom:6px}
.form-input,.form-textarea{width:100%;padding:13px;background:rgba(20,12,5,.9);border:1.5px solid rgba(212,135,28,.25);border-radius:10px;color:#FFF8E7;font-size:14px;outline:none;transition:all .2s;box-shadow:inset 0 2px 4px rgba(0,0,0,.2)}
.form-input:focus,.form-textarea:focus{border-color:#F4C430;box-shadow:inset 0 2px 4px rgba(0,0,0,.2),0 0 8px rgba(244,196,48,.2)}
.form-textarea{min-height:100px;resize:vertical;font-family:inherit}
select.form-input{appearance:none;-webkit-appearance:none}
/* Buttons — пивные этикетки */
.btn{width:100%;padding:15px;border-radius:12px;border:none;font-size:15px;font-weight:700;cursor:pointer;transition:all .2s;letter-spacing:.5px;position:relative;overflow:hidden}
.btn::before{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.15),transparent);transition:left .5s}
.btn:active::before{left:100%}
.btn-primary{background:linear-gradient(135deg,#D4871C,#B8860B,#C9A84C);color:#1A1209;box-shadow:0 3px 12px rgba(212,135,28,.35),inset 0 1px 0 rgba(255,248,231,.3);text-shadow:0 1px 0 rgba(255,255,255,.2);border:1px solid rgba(244,196,48,.4)}
.btn-danger{background:linear-gradient(135deg,#C62828,#B71C1C,#E53935);color:#FFF;box-shadow:0 3px 12px rgba(198,40,40,.3);border:1px solid rgba(229,57,53,.4)}
.btn:active{transform:scale(.96);box-shadow:none}
.btn:disabled{opacity:.5;pointer-events:none}
/* Offer cards */
.offer-card{background:linear-gradient(145deg,rgba(55,35,12,.9),rgba(40,25,10,.95));border:1.5px solid rgba(212,135,28,.25);border-radius:14px;padding:16px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 8px rgba(0,0,0,.2)}
.offer-name{font-size:14px;font-weight:700;color:#FFF8E7}
.offer-rate{font-size:13px;color:#F4C430;font-weight:600}
.offer-apply{padding:9px 18px;background:linear-gradient(135deg,rgba(212,135,28,.2),rgba(184,115,51,.15));border:1.5px solid rgba(244,196,48,.4);border-radius:10px;color:#F4C430;font-size:12px;font-weight:700;cursor:pointer;letter-spacing:.3px;transition:all .2s}
.offer-apply:active{background:rgba(212,135,28,.35);transform:scale(.95)}
/* Menu items — пивная карта */
.menu-item{display:flex;align-items:center;gap:14px;padding:16px;background:linear-gradient(145deg,rgba(55,35,12,.9),rgba(40,25,10,.95));border:1.5px solid rgba(212,135,28,.2);border-radius:14px;margin-bottom:10px;cursor:pointer;transition:all .2s;box-shadow:0 2px 8px rgba(0,0,0,.2)}
.menu-item:active{background:linear-gradient(145deg,rgba(65,42,15,.95),rgba(50,30,12,.98));transform:scale(.97);border-color:rgba(244,196,48,.4)}
.menu-item:hover{border-color:rgba(244,196,48,.4);box-shadow:0 4px 15px rgba(212,135,28,.15)}
.menu-icon{font-size:26px;width:42px;text-align:center;filter:drop-shadow(0 0 8px rgba(244,196,48,.4));transition:all .3s ease}.menu-item:active .menu-icon{transform:scale(1.2) rotate(5deg);filter:drop-shadow(0 0 15px rgba(244,196,48,.8))}
.menu-text{font-size:14px;font-weight:600;color:#FFF8E7;letter-spacing:.3px}
.menu-arrow{margin-left:auto;color:#F4C430;font-size:16px;font-weight:700}
/* AI Chat */
.chat-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px}
.chat-msg{max-width:85%;padding:10px 14px;border-radius:12px;font-size:13px;line-height:1.5;animation:fadeIn .3s}
.chat-msg.user{align-self:flex-end;background:linear-gradient(135deg,rgba(212,135,28,.3),rgba(184,115,51,.2));border:1px solid rgba(244,196,48,.35);color:#FFF8E7}
.chat-msg.bot{align-self:flex-start;background:linear-gradient(145deg,rgba(50,32,12,.95),rgba(35,22,10,.9));border:1px solid rgba(212,135,28,.2);color:#C9A84C}
.chat-input-area{display:flex;gap:8px;padding:12px 16px;background:rgba(42,30,18,.95);border-top:1px solid rgba(212,135,28,.2)}
.chat-input{flex:1;padding:10px 14px;background:rgba(26,18,9,.8);border:1px solid rgba(212,135,28,.3);border-radius:20px;color:#FFF8E7;font-size:14px;outline:none}
.chat-send{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#D4871C,#C9A84C);border:none;color:#1A1209;font-size:18px;cursor:pointer}
/* Achievement badges */
.badge{display:inline-flex;align-items:center;gap:4px;padding:4px 10px;background:rgba(212,135,28,.15);border:1px solid rgba(212,135,28,.2);border-radius:20px;font-size:12px;color:#C9A84C;margin:3px}
/* Channel check overlay */
.gate-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:linear-gradient(180deg,#1A1209 0%,#2A1A0A 40%,#0F0A04 100%);z-index:200;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;text-align:center}
.gate-icon{font-size:72px;margin-bottom:20px;animation:iconFloat 3s ease-in-out infinite,beerGlow 2.5s ease-in-out infinite}
.gate-title{font-size:24px;font-weight:700;color:#F4C430;margin-bottom:12px;text-shadow:0 0 12px rgba(244,196,48,.4);letter-spacing:1px}
.gate-text{font-size:14px;color:#C9A84C;margin-bottom:24px;line-height:1.6}
.gate-btn{display:inline-block;padding:15px 36px;background:linear-gradient(135deg,#D4871C,#B8860B,#C9A84C);color:#1A1209;border-radius:12px;font-size:15px;font-weight:700;text-decoration:none;cursor:pointer;border:1px solid rgba(244,196,48,.4);margin-bottom:12px;box-shadow:0 4px 15px rgba(212,135,28,.35);letter-spacing:.5px}
.gate-btn-outline{display:inline-block;padding:12px 28px;background:rgba(212,135,28,.08);border:1.5px solid rgba(244,196,48,.4);color:#F4C430;border-radius:12px;font-size:14px;font-weight:600;cursor:pointer;text-decoration:none;transition:all .2s}
.gate-btn-outline:active{background:rgba(212,135,28,.2)}
/* Captcha */
.captcha-box{background:linear-gradient(145deg,rgba(55,35,12,.95),rgba(35,22,10,.98));border:2px solid rgba(244,196,48,.4);border-radius:18px;padding:28px;max-width:320px;width:100%;box-shadow:0 6px 25px rgba(0,0,0,.4),0 0 20px rgba(244,196,48,.1)}
.captcha-question{font-size:20px;color:#F4C430;margin-bottom:18px;font-weight:700;text-shadow:0 0 8px rgba(244,196,48,.3)}
.captcha-options{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.captcha-opt{padding:16px;background:linear-gradient(135deg,rgba(212,135,28,.1),rgba(184,115,51,.08));border:1.5px solid rgba(212,135,28,.35);border-radius:12px;color:#FFF8E7;font-size:17px;font-weight:700;cursor:pointer;text-align:center;transition:all .2s}
.captcha-opt:active{background:rgba(212,135,28,.3);transform:scale(.93);border-color:rgba(244,196,48,.6)}
.captcha-opt.wrong{background:rgba(198,40,40,.3);border-color:rgba(198,40,40,.5)}
.captcha-opt.correct{background:rgba(46,125,50,.3);border-color:rgba(46,125,50,.5)}
/* Loader */
.loader{width:32px;height:32px;border:3px solid rgba(212,135,28,.2);border-top-color:#D4871C;border-radius:50%;animation:spin .8s linear infinite;margin:20px auto}
/* Toast */
.toast{position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,rgba(50,30,12,.98),rgba(35,22,10,.98));border:1.5px solid rgba(244,196,48,.5);padding:12px 24px;border-radius:12px;font-size:13px;color:#FFF8E7;z-index:300;animation:fadeIn .3s;pointer-events:none;box-shadow:0 4px 20px rgba(0,0,0,.5),0 0 15px rgba(244,196,48,.15)}
/* University */
.lesson-card{background:rgba(42,30,18,.9);border:1px solid rgba(212,135,28,.2);border-radius:12px;padding:16px;margin-bottom:10px;cursor:pointer;transition:all .2s}
.lesson-card:active{transform:scale(.98)}
.lesson-num{font-size:12px;color:#C9A84C;margin-bottom:4px}
.lesson-title{font-size:15px;font-weight:600;color:#FFF8E7}
.lesson-reward{font-size:12px;color:#D4871C;margin-top:4px}
/* Fix scroll in sections */
.content{height:calc(100vh - 70px);overflow-y:auto;-webkit-overflow-scrolling:touch}
.overlay-bg{display:flex;flex-direction:column;height:100vh;overflow:hidden}
/* Header split layout */
.header-info{display:flex;justify-content:space-between;align-items:center;padding:0 8px}
.user-info-left{text-align:left}
.balance-right{text-align:right}
.balance-amount{font-size:22px;font-weight:700;color:#F4C430;text-shadow:0 0 10px rgba(244,196,48,.4)}
.balance-label{font-size:11px;color:#C9A84C}
/* Achievement card unlocked/locked */
.achievement-locked{opacity:.6;filter:grayscale(.4)}
.achievement-unlocked{border-color:rgba(244,196,48,.6)!important;box-shadow:0 0 15px rgba(244,196,48,.25)}
.achievements-section-title{font-size:14px;font-weight:700;color:#C9A84C;margin:16px 0 8px;padding-left:4px;text-transform:uppercase;letter-spacing:1px}
/* Referral stats */
.ref-recent{padding:8px 0;border-bottom:1px solid rgba(212,135,28,.1)}
.ref-recent-name{font-size:13px;color:#FFF8E7}
.ref-recent-date{font-size:11px;color:#C9A84C}
/* Lesson content */
.lesson-content{padding:16px;font-size:14px;color:#C9A84C;line-height:1.7}
.quiz-option{padding:12px;background:rgba(212,135,28,.08);border:1.5px solid rgba(212,135,28,.25);border-radius:10px;margin-bottom:8px;cursor:pointer;color:#FFF8E7;font-size:14px;transition:all .2s}
.quiz-option:active{transform:scale(.97)}
.quiz-option.correct{background:rgba(46,125,50,.3);border-color:rgba(46,125,50,.5)}
.quiz-option.wrong{background:rgba(198,40,40,.3);border-color:rgba(198,40,40,.5)}
.quiz-question{font-size:15px;font-weight:600;color:#F4C430;margin:16px 0 10px}
/* Premium Exam Styles */
.exam-start-btn{display:block;width:100%;padding:16px;margin-top:20px;background:linear-gradient(135deg,#D4871C,#F4C430);border:none;border-radius:14px;color:#1A1209;font-size:18px;font-weight:700;cursor:pointer;position:relative;overflow:hidden;transition:all .3s ease;animation:examPulse 2s ease-in-out infinite}
.exam-start-btn:hover{transform:scale(1.03);box-shadow:0 0 25px rgba(244,196,48,.4)}
.exam-start-btn:active{transform:scale(.97)}
.exam-start-btn::after{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:linear-gradient(45deg,transparent,rgba(255,255,255,.15),transparent);transform:rotate(45deg);animation:shimmer 3s infinite}
@keyframes examPulse{0%,100%{box-shadow:0 0 10px rgba(244,196,48,.3)}50%{box-shadow:0 0 25px rgba(244,196,48,.5)}}
@keyframes shimmer{0%{background-position:200% center}100%{background-position:-200% center}}
@keyframes slideInRight{from{opacity:0;transform:translateX(60px)}to{opacity:1;transform:translateX(0)}}
@keyframes scaleIn{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:scale(1)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes confettiDrop{0%{transform:translateY(-100vh) rotate(0deg);opacity:1}100%{transform:translateY(100vh) rotate(720deg);opacity:0}}
@keyframes progressGlow{0%{background-position:0% 50%}100%{background-position:200% 50%}}
.exam-progress-bar{height:6px;border-radius:3px;background:rgba(255,255,255,.1);margin-bottom:16px;overflow:hidden}
.exam-progress-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,#D4871C,#F4C430,#D4871C);background-size:200% 100%;animation:progressGlow 2s linear infinite;transition:width .5s ease}
.exam-question-num{font-size:13px;color:#C9A84C;margin-bottom:4px}
.exam-slide{animation:slideInRight .4s ease}
.confetti-piece{position:fixed;width:10px;height:10px;top:-10px;z-index:10000;border-radius:2px;animation:confettiDrop 3s linear forwards}
</style>
</head>
<body>

<!-- Beer Bubbles Background -->
<div class="bubbles" id="bubbles"></div>

<!-- GATE: Channel Check DISABLED for test -->

<!-- ===== GATE: Captcha ===== -->
<div class="gate-overlay" id="gateCaptcha" style="display:none">
  <div class="gate-icon">🔒</div>
  <div class="gate-title">Проверка</div>
  <div class="gate-text">Решите пример для входа</div>
  <div class="captcha-box">
    <div class="captcha-question" id="captchaQ"></div>
    <div class="captcha-options" id="captchaOpts"></div>
  </div>
  <div id="captchaError" style="color:#E53935;font-size:12px;margin-top:12px;display:none"></div>
</div>

<!-- ===== GATE: Loading ===== -->
<div class="gate-overlay" id="gateLoading">
  <div class="gate-icon">🍺</div>
  <div class="gate-title">CRAFT V2.0</div>
  <div class="loader"></div>
  <div class="gate-text">Загрузка...</div>
</div>

<!-- ===== MAIN SCREEN ===== -->
<div class="screen" id="screenMain">
  <div class="header">
    <div class="header-info">
      <div class="user-info-left">
        <div class="uid" id="userUID">#0000</div>
        <div style="font-size:12px;color:#C9A84C" id="userUsername">@username</div>
        <div style="font-size:11px;color:#8B7355" id="userNickname"></div>
      </div>
      <div class="balance-right">
        <div class="balance-amount"><span id="userBalance">0</span> 🍺</div>
        <div class="balance-label">крышек</div>
      </div>
    </div>
  </div>
  <div class="main-grid fade-in">
    <div class="main-block" onclick="showScreen('cabinet')">
      <div class="block-icon">🍺</div><div class="block-title">Личный кабинет</div>
    </div>
    <div class="main-block" onclick="showScreen('connection')">
      <div class="block-icon">🍻</div><div class="block-title">Подключение</div>
    </div>
    <div class="main-block sos-block" onclick="showScreen('sos')">
      <div class="block-icon">🚨</div><div class="block-title">SOS</div>
    </div>
    <div class="main-block" onclick="showScreen('menu')">
      <div class="block-icon">📋</div><div class="block-title">Барная карта</div>
    </div>
  </div>
  <div class="footer">
    <a class="footer-btn" onclick="openChannelLink()">📻 Канал</a>
    <a class="footer-btn" onclick="showScreen('support')">🛎️ Поддержка</a>
  </div>
</div>

<!-- ===== CABINET SCREEN ===== -->
<div class="overlay" id="screenCabinet">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('main')">←</button>
      <div class="sub-title">🍺 Личный кабинет</div>
    </div>
    <div class="content fade-in" id="cabinetContent">
      <div class="loader"></div>
    </div>
  </div>
</div>

<!-- ===== CONNECTION SCREEN ===== -->
<div class="overlay" id="screenConnection">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('main')">←</button>
      <div class="sub-title">🍻 Подключение</div>
    </div>
    <div class="content fade-in" id="connectionContent">
      <div class="card" style="border-color:rgba(212,175,55,.5);background:linear-gradient(135deg,rgba(42,30,18,.95),rgba(50,35,15,.95))">
        <div style="text-align:center;margin-bottom:16px">
          <div style="font-size:42px;animation:beerGlow 2s ease-in-out infinite">🍺</div>
          <div style="font-size:20px;font-weight:700;color:#D4871C;margin-top:8px">CRAFT - Geotransfer</div>
          <div style="font-size:13px;color:#C9A84C;margin-top:4px">Подключение к площадке Geotransfer</div>
        </div>
        <div style="background:rgba(26,18,9,.6);border-radius:10px;padding:14px;margin-bottom:12px">
          <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(212,135,28,.15)">
            <span style="font-size:14px;color:#C9A84C">📝 Чеки 1-10к</span>
            <span style="font-size:16px;font-weight:700;color:#FFF8E7">12-14%</span>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(212,135,28,.15)">
            <span style="font-size:14px;color:#C9A84C">📝 Чеки 10к+</span>
            <span style="font-size:16px;font-weight:700;color:#FFF8E7">8-9%</span>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(212,135,28,.15)">
            <span style="font-size:14px;color:#C9A84C">📱 Сим</span>
            <span style="font-size:16px;font-weight:700;color:#FFF8E7">15%</span>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(212,135,28,.15)">
            <span style="font-size:14px;color:#C9A84C">📲 QR/НСПК</span>
            <span style="font-size:16px;font-weight:700;color:#FFF8E7">12-13%</span>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(212,135,28,.15)">
            <span style="font-size:14px;color:#C9A84C">🛡️ Страховой депозит</span>
            <span style="font-size:16px;font-weight:700;color:#FFF8E7">500$</span>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0">
            <span style="font-size:14px;color:#C9A84C">💼 Рабочий депозит</span>
            <span style="font-size:16px;font-weight:700;color:#FFF8E7">от 300$</span>
          </div>
        </div>
        <button class="btn btn-primary" onclick="showScreen('appForm')" style="animation:beerGlow 2s ease-in-out infinite">📋 Подать заявку</button>
      </div>
    </div>
  </div>
</div>

<!-- ===== APPLICATION FORM (Step-by-step) ===== -->
<div class="overlay" id="screenAppForm">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="appFormBack()">←</button>
      <div class="sub-title">📋 Анкета <span id="appStepLabel">1/6</span></div>
    </div>
    <div class="content fade-in">
      <!-- Progress bar -->
      <div style="background:rgba(26,18,9,.8);border-radius:8px;height:6px;margin-bottom:20px;overflow:hidden">
        <div id="appProgress" style="height:100%;background:linear-gradient(90deg,#D4871C,#C9A84C);border-radius:8px;transition:width .3s;width:16.6%"></div>
      </div>
      <div class="card" style="border-color:rgba(212,135,28,.4)">
        <div class="card-title" id="appQuestionTitle">Вопрос 1 из 6</div>
        <div id="appQuestionText" style="font-size:15px;color:#FFF8E7;margin:12px 0 16px;line-height:1.5"></div>
        <div class="form-group">
          <textarea class="form-textarea" id="appAnswer" placeholder="Ваш ответ..." style="min-height:80px"></textarea>
        </div>
        <button class="btn btn-primary" id="appNextBtn" onclick="appFormNext()">Далее →</button>
      </div>
    </div>
  </div>
</div>

<!-- ===== SOS SCREEN ===== -->
<div class="overlay" id="screenSos">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('main')">←</button>
      <div class="sub-title">🆘 SOS</div>
    </div>
    <div class="content fade-in">
      <div class="card" style="border-color:rgba(198,40,40,.4)">
        <div class="card-title" style="color:#E53935">🆘 Экстренная помощь</div>
        <div class="card-text" style="margin-bottom:16px">Блокировка? Проблема? Опишите ситуацию — мы поможем максимально быстро</div>
        <div class="form-group">
          <label class="form-label">Город</label>
          <input class="form-input" id="sosCity" placeholder="Ваш город">
        </div>
        <div class="form-group">
          <label class="form-label">Контакт для связи</label>
          <input class="form-input" id="sosContact" placeholder="@username или телефон">
        </div>
        <div class="form-group">
          <label class="form-label">Описание проблемы</label>
          <textarea class="form-textarea" id="sosDesc" placeholder="Что случилось? Опишите подробно"></textarea>
        </div>
        <button class="btn btn-danger" id="sosSubmitBtn" onclick="submitSOS()">🆘 Отправить SOS</button>
      </div>
    </div>
  </div>
</div>

<!-- ===== MENU SCREEN ===== -->
<div class="overlay" id="screenMenu">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('main')">←</button>
      <div class="sub-title">🍺 Барная карта</div>
    </div>
    <div class="content fade-in">
      <div class="menu-item" onclick="showScreen('ai')">
        <div class="menu-icon">🍻</div>
        <div class="menu-text">ИИ Помощник (Михалыч)</div>
        <div class="menu-arrow">›</div>
      </div>
      <div class="menu-item" onclick="showScreen('university')">
        <div class="menu-icon">🏫</div>
        <div class="menu-text">Университет CRAFT</div>
        <div class="menu-arrow">›</div>
      </div>
      <div class="menu-item" onclick="showScreen('shop')">
        <div class="menu-icon">🛒</div>
        <div class="menu-text">Магазин</div>
        <div class="menu-arrow">›</div>
      </div>
      <div class="menu-item" onclick="showScreen('referral')">
        <div class="menu-icon">🤝</div>
        <div class="menu-text">Реферальная программа</div>
        <div class="menu-arrow">›</div>
      </div>
      <div class="menu-item" onclick="showScreen('achievements')">
        <div class="menu-icon">🏆</div>
        <div class="menu-text">Достижения</div>
        <div class="menu-arrow">›</div>
      </div>
      <div class="menu-item" onclick="showScreen('news')">
        <div class="menu-icon">📰</div>
        <div class="menu-text">Новости</div>
        <div class="menu-arrow">›</div>
      </div>
      <div class="menu-item" onclick="showScreen('support')">
        <div class="menu-icon">🛎️</div>
        <div class="menu-text">Техподдержка</div>
        <div class="menu-arrow">›</div>
      </div>
      <div class="menu-item" onclick="openChannelLink()">
        <div class="menu-icon">📻</div>
        <div class="menu-text">Наш канал</div>
        <div class="menu-arrow">›</div>
      </div>
    </div>
  </div>
</div>

<!-- ===== AI CHAT ===== -->
<div class="overlay" id="screenAi">
  <div class="overlay-bg" style="display:flex;flex-direction:column;height:100vh">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('menu')">←</button>
      <div class="sub-title">🍻 Михалыч</div>
      <div style="margin-left:auto;font-size:11px;color:#C9A84C">5 🍺/msg</div>
    </div>
    <div class="chat-messages" id="chatMessages">
      <div class="chat-msg bot">Привет! Я Михалыч 🍺 — ИИ-помощник CRAFT. Спрашивай что угодно по теме процессинга, блокировок, схем работы. Каждое сообщение стоит 5 крышек.</div>
    </div>
    <div class="chat-input-area">
      <input class="chat-input" id="chatInput" placeholder="Сообщение..." onkeypress="if(event.key==='Enter')sendChat()">
      <button class="chat-send" onclick="sendChat()">➤</button>
    </div>
  </div>
</div>

<!-- ===== UNIVERSITY ===== -->
<div class="overlay" id="screenUniversity">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('menu')">←</button>
      <div class="sub-title">🏫 Университет</div>
    </div>
    <div class="content fade-in" id="universityContent">
      <div class="loader"></div>
    </div>
  </div>
</div>

<!-- ===== REFERRAL ===== -->
<div class="overlay" id="screenReferral">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('menu')">←</button>
      <div class="sub-title">🤝 Рефералы</div>
    </div>
    <div class="content fade-in" id="referralContent">
      <div class="loader"></div>
    </div>
  </div>
</div>

<!-- ===== ACHIEVEMENTS ===== -->
<div class="overlay" id="screenAchievements">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('menu')">←</button>
      <div class="sub-title">🏆 Достижения</div>
    </div>
    <div class="content fade-in" id="achievementsContent">
      <div class="loader"></div>
    </div>
  </div>
</div>

<!-- ===== SUPPORT ===== -->
<div class="overlay" id="screenSupport">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('main')">←</button>
      <div class="sub-title">🛎️ Поддержка</div>
    </div>
    <div class="content fade-in">
      <div class="card">
        <div class="card-title">🛎️ Напишите нам</div>
        <div class="card-text" style="margin-bottom:12px">Опишите вашу проблему или вопрос</div>
        <div style="padding:12px;margin-bottom:16px;border-radius:10px;background:rgba(212,135,28,0.08);border:1px solid rgba(212,135,28,0.15);font-size:13px;color:#C9A84C;line-height:1.6">
        💡 <b>Есть идея или предложение?</b><br>Мы всегда открыты к улучшениям! Напишите что хотели бы видеть в CRAFT — новые функции, уроки, инструменты. Каждое сообщение читается лично командой.<br><br>📩 Техподдержка · 💡 Идеи · 🐛 Баг-репорты</div>
        <div class="form-group">
          <textarea class="form-textarea" id="supportMsg" placeholder="Ваше сообщение..."></textarea>
        </div>
        <button class="btn btn-primary" id="supportBtn" onclick="submitSupport()">📨 Отправить</button>
      </div>
    </div>
  </div>
</div>

<div class="overlay" id="screenShop">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('menu')">←</button>
      <div class="sub-title">🛒 Магазин</div>
      <div id="cartBadge" onclick="showShopCart()" style="position:absolute;right:16px;top:50%;transform:translateY(-50%);font-size:22px;cursor:pointer">🛒 <span id="cartCount" style="background:#D4871C;color:#fff;border-radius:50%;padding:2px 7px;font-size:12px;font-weight:700;display:none">0</span></div>
    </div>
    <div class="content fade-in">
      <div style="margin-bottom:10px"><button onclick="showScreen('purchaseHistory')" style="padding:8px 14px;border-radius:10px;border:1px solid rgba(212,135,28,.3);background:rgba(212,135,28,.1);color:#F4C430;font-size:12px;cursor:pointer">📋 Мои покупки</button></div>
      <div id="shopTabs" style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px">
        <button class="shop-tab active" onclick="filterShop('all',this)" style="padding:6px 12px;border-radius:20px;border:1px solid rgba(212,135,28,.4);background:rgba(212,135,28,.2);color:#F4C430;font-size:12px;cursor:pointer;font-weight:600">Все</button>
        <button class="shop-tab" onclick="filterShop('manuals',this)" style="padding:6px 12px;border-radius:20px;border:1px solid rgba(212,135,28,.2);background:transparent;color:#C9A84C;font-size:12px;cursor:pointer">Мануалы</button>
        <button class="shop-tab" onclick="filterShop('private',this)" style="padding:6px 12px;border-radius:20px;border:1px solid rgba(212,135,28,.2);background:transparent;color:#C9A84C;font-size:12px;cursor:pointer">Приватка</button>
        <button class="shop-tab" onclick="filterShop('schemes',this)" style="padding:6px 12px;border-radius:20px;border:1px solid rgba(212,135,28,.2);background:transparent;color:#C9A84C;font-size:12px;cursor:pointer">Доп. Схемы</button>
        <button class="shop-tab" onclick="filterShop('training',this)" style="padding:6px 12px;border-radius:20px;border:1px solid rgba(212,135,28,.2);background:transparent;color:#C9A84C;font-size:12px;cursor:pointer">Обучи</button>
        <button class="shop-tab" onclick="filterShop('contacts',this)" style="padding:6px 12px;border-radius:20px;border:1px solid rgba(212,135,28,.2);background:transparent;color:#C9A84C;font-size:12px;cursor:pointer">Контакты</button>
        <button class="shop-tab" onclick="filterShop('tables',this)" style="padding:6px 12px;border-radius:20px;border:1px solid rgba(212,135,28,.2);background:transparent;color:#C9A84C;font-size:12px;cursor:pointer">Таблички</button>
      </div>
      <div id="shopItems" style="display:flex;flex-direction:column;gap:10px"></div>
    </div>
  </div>
</div>

<div class="overlay" id="screenCart">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('shop')">←</button>
      <div class="sub-title">🛒 Корзина</div>
    </div>
    <div class="content fade-in">
      <div id="cartItems" style="display:flex;flex-direction:column;gap:10px"></div>
      <div id="cartTotal" style="text-align:center;margin:16px 0;font-size:18px;font-weight:700;color:#F4C430"></div>
      <button class="btn btn-primary" id="checkoutBtn" onclick="shopCheckout()" style="display:none">💰 Купить</button>
    </div>
  </div>
</div>

<!-- ===== NEWS SCREEN ===== -->
<div class="overlay" id="screenNews">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('menu')">←</button>
      <div class="sub-title">📰 Новости</div>
    </div>
    <div class="content fade-in" id="newsContent">
      <div class="loader"></div>
    </div>
  </div>
</div>

<!-- Toast -->
<div class="toast" id="toast" style="display:none"></div>

<script>
/* ============ STATE ============ */
const APP = {
  tgId: null, uid: null, balance: 0, firstName: '', lastName: '', username: '',
  profile: null, channelOk: true, captchaOk: false, ready: false
};
const CHANNEL_LINK = 'https://t.me/+MepEj5pb6kU3OGI1';
const API = '';

/* ============ TELEGRAM ============ */
let tg = null;
if (typeof Telegram !== 'undefined' && Telegram.WebApp) {
  tg = Telegram.WebApp;
  tg.ready(); tg.expand();
  try { tg.setHeaderColor('#2C1F0E'); tg.setBackgroundColor('#1A1209'); } catch(e){}
}
function getReferrerUid() {
  const urlParams = new URLSearchParams(window.location.search);
  let startParam = urlParams.get('tgWebAppStartParam');
  if (!startParam && tg && tg.initDataUnsafe) startParam = tg.initDataUnsafe.start_param;
  if (!startParam) { const ref = urlParams.get('ref'); if (ref) return ref; }
  if (startParam && startParam.startsWith('ref_')) {
    const uid = startParam.replace('ref_', '');
    try { localStorage.setItem('craft_referral_uid', uid); } catch(e){}
    return uid;
  }
  try { return localStorage.getItem('craft_referral_uid'); } catch(e){ return null; }
}
function getTgData() {
  if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
    const u = tg.initDataUnsafe.user;
    return { telegram_id: u.id.toString(), first_name: u.first_name||'', last_name: u.last_name||'', username: u.username||'', referrer_uid: getReferrerUid() };
  }
  return { telegram_id: 'demo_' + Date.now() };
}

/* ============ INIT FLOW ============ */
document.addEventListener('DOMContentLoaded', startApp);
async function startApp() {
  const d = getTgData();
  APP.tgId = d.telegram_id;
  APP.firstName = d.first_name; APP.lastName = d.last_name; APP.username = d.username;
  
  // 1. Init user on server
  try {
    const r = await api('/api/init', d);
    if (r && r.success) {
      APP.uid = r.system_uid; APP.balance = r.caps_balance;
      APP.isNewsSubscriber = r.is_news_subscriber || false;
      APP.userLevel = r.user_level || 'basic';
      // Track visits for news popup
      const visitKey = 'craft_visit_count_' + APP.tgId;
      const visits = parseInt(localStorage.getItem(visitKey) || '0') + 1;
      localStorage.setItem(visitKey, visits);
      APP.visitCount = visits;
    }
  } catch(e) { console.error('Init failed', e); }
  
  // 2. Channel subscription check
  try {
    const chRes = await api('/api/channel/check', { telegram_id: APP.tgId });
    if (chRes.subscribed) {
      APP.channelOk = true;
      try { hide('gateLoading'); } catch(e) {}
      showCaptcha();
    } else {
      APP.channelOk = false;
      try { hide('gateLoading'); } catch(e) {}
      show('gateChannel');
    }
  } catch(e) {
    // If check fails, let user through
    APP.channelOk = true;
    try { hide('gateLoading'); } catch(e2) {}
    showCaptcha();
  }
}

/* ============ CHANNEL CHECK ============ */
function openChannelLink() {
  if (tg) { tg.openTelegramLink(CHANNEL_LINK); }
  else { window.open(CHANNEL_LINK, '_blank'); }
}
async function recheckSubscription() {
  const errEl = document.getElementById('channelError');
  errEl.style.display = 'none';
  try {
    const r = await api('/api/check-subscription', { telegram_id: APP.tgId });
    if (r.subscribed) {
      APP.channelOk = true;
      hide('gateChannel');
      showCaptcha();
    } else {
      errEl.textContent = 'Подписка не найдена. Подпишитесь и попробуйте снова.';
      errEl.style.display = 'block';
    }
  } catch(e) {
    errEl.textContent = 'Ошибка проверки. Попробуйте ещё раз.';
    errEl.style.display = 'block';
  }
}

/* ============ CAPTCHA ============ */
let captchaAnswer = 0;
function showCaptcha() {
  const a = Math.floor(Math.random()*20)+1;
  const b = Math.floor(Math.random()*20)+1;
  captchaAnswer = a + b;
  document.getElementById('captchaQ').textContent = a + ' + ' + b + ' = ?';
  
  const opts = new Set([captchaAnswer]);
  while(opts.size < 4) opts.add(Math.floor(Math.random()*40)+2);
  const arr = Array.from(opts).sort(()=>Math.random()-.5);
  
  const container = document.getElementById('captchaOpts');
  container.innerHTML = '';
  arr.forEach(v => {
    const btn = document.createElement('div');
    btn.className = 'captcha-opt';
    btn.textContent = v;
    btn.onclick = () => checkCaptcha(v, btn);
    container.appendChild(btn);
  });
  show('gateCaptcha');
}
function checkCaptcha(val, btn) {
  if (val === captchaAnswer) {
    btn.classList.add('correct');
    APP.captchaOk = true;
    setTimeout(() => {
      hide('gateCaptcha');
      enterApp();
    }, 400);
  } else {
    btn.classList.add('wrong');
    const errEl = document.getElementById('captchaError');
    errEl.textContent = 'Неверно! Попробуйте ещё раз';
    errEl.style.display = 'block';
    setTimeout(() => { btn.classList.remove('wrong'); errEl.style.display = 'none'; }, 1000);
  }
}

/* ============ ENTER APP ============ */
function enterApp() {
  document.getElementById('userUID').textContent = '#' + (APP.uid || '0000');
  document.getElementById('userBalance').textContent = APP.balance || 0;
  document.getElementById('userUsername').textContent = APP.username ? '@'+APP.username : '';
  document.getElementById('userNickname').textContent = APP.firstName || '';
  document.getElementById('screenMain').classList.add('active');
  APP.ready = true;
  
  // Show news subscription popup on 2nd+ visit if not subscribed
  if (APP.visitCount >= 2 && !APP.isNewsSubscriber) {
    setTimeout(() => showNewsPopup(), 800);
  }
}

function showNewsPopup() {
  const existing = document.getElementById('newsPopupOverlay');
  if (existing) existing.remove();
  
  const overlay = document.createElement('div');
  overlay.id = 'newsPopupOverlay';
  overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.7);z-index:9999;display:flex;align-items:center;justify-content:center;animation:fadeIn 0.3s ease';
  overlay.innerHTML = `
    <div style="background:linear-gradient(135deg,#1A0E0A,#2A1810);border:1px solid rgba(212,135,28,0.3);border-radius:16px;padding:24px;margin:20px;max-width:340px;text-align:center;animation:slideInUp 0.4s ease">
      <div style="font-size:36px;margin-bottom:12px">📰</div>
      <h3 style="color:#F4C430;margin:0 0 8px;font-size:18px">Подпишись на новости!</h3>
      <p style="color:#ccc;font-size:14px;margin:0 0 16px;line-height:1.4">Ежедневный дайджест по рынку: ситуация, методы, мануалы. Всё важное — без воды.</p>
      <p style="color:#D4871C;font-size:13px;margin:0 0 16px">💰 10 крышек/день</p>
      <button onclick="showScreen('news');document.getElementById('newsPopupOverlay').remove()" style="background:linear-gradient(135deg,#D4871C,#F4C430);color:#1A0E0A;border:none;padding:12px 24px;border-radius:10px;font-weight:bold;font-size:15px;cursor:pointer;width:100%;margin-bottom:8px">📰 Подписаться</button>
      <button onclick="document.getElementById('newsPopupOverlay').remove()" style="background:transparent;color:#888;border:none;padding:8px;font-size:13px;cursor:pointer;width:100%">Позже</button>
    </div>
  `;
  document.body.appendChild(overlay);
}

/* ============ NAVIGATION ============ */
function showScreen(name) {
  // Close all overlays
  document.querySelectorAll('.overlay').forEach(el => el.classList.remove('active'));
  
  if (name === 'main') {
    updateBalance();
    return;
  }
  
  const screenId = 'screen' + name.charAt(0).toUpperCase() + name.slice(1);
  const el = document.getElementById(screenId);
  if (el) {
    el.classList.add('active');
    // Load content for specific screens
    if (name === 'cabinet') loadCabinet();
    if (name === 'connection') loadConnection();
    if (name === 'university') loadUniversity();
    if (name === 'referral') loadReferral();
    if (name === 'achievements') loadAchievements();
    if (name === 'appForm') initAppForm();
    if (name === 'shop') loadShopItems();
    if (name === 'cart') loadShopCart();
    if (name === 'purchaseHistory') loadPurchaseHistory();
    if (name === 'balanceHistory') loadBalanceHistory('all');
    if (name === 'news') loadNews();
  }
}
function updateBalance() {
  document.getElementById('userBalance').textContent = APP.balance || 0;
}

/* ============ CABINET ============ */
async function loadCabinet() {
  const el = document.getElementById('cabinetContent');
  el.innerHTML = '<div class="loader"></div>';
  try {
    const r = await api('/api/user/profile?telegram_id=' + APP.tgId, null, 'GET');
    if (r.success) {
      const p = r.profile;
      APP.profile = p;
      el.innerHTML = `
        <div class="card">
          <div style="text-align:center;margin-bottom:12px">
            <div style="font-size:48px;animation:iconPulse 2s ease-in-out infinite">🍺</div>
            <div style="font-size:20px;font-weight:700;color:#D4871C;margin-top:8px">#${p.system_uid}</div>
            ${p.user_level === 'vip' ? '<div style="font-size:14px;font-weight:700;color:#FFD700;margin-top:4px;text-shadow:0 0 10px rgba(255,215,0,.5)">👑 VIP</div>' : ''}
            <div style="font-size:14px;color:#C9A84C">${p.first_name||''} ${p.last_name||''}</div>
            ${p.username ? '<div style="font-size:12px;color:#C9A84C">@'+p.username+'</div>' : ''}
          </div>
          <div style="text-align:center;margin:8px 0;padding:8px;border-radius:8px;background:${p.user_level==='vip'?'linear-gradient(135deg,rgba(255,215,0,0.15),rgba(212,135,28,0.15))':'rgba(255,255,255,0.05)'};border:1px solid ${p.user_level==='vip'?'rgba(255,215,0,0.3)':'rgba(255,255,255,0.1)'}">
            <div style="font-size:12px;color:#888">Ваш уровень</div>
            <div style="font-size:16px;font-weight:700;color:${p.user_level==='vip'?'#FFD700':'#D4871C'}">${p.user_level==='vip'?'👑 VIP — безлимит ИИ':'🍺 Базовый — 5 крышек/сообщение'}</div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">💰 Баланс</div>
          <div class="card-value">${p.caps_balance} крышек 🍺</div>
          <div class="stat-row"><span class="stat-label">Заработано всего</span><span class="stat-val">${p.total_earned_caps} 🍺</span></div>
          <div class="stat-row"><span class="stat-label">Потрачено</span><span class="stat-val">${p.total_spent_caps} 🍺</span></div>
          <div class="stat-row"><span class="stat-label">Запросов к ИИ</span><span class="stat-val">${p.ai_requests_count}</span></div>
        </div>
        <div class="card" onclick="showScreen('balanceHistory')" style="cursor:pointer">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div class="card-title">📊 История баланса</div>
            <div style="font-size:18px;color:#C9A84C">›</div>
          </div>
        </div>
        <div class="card">
          <div class="card-title">🏆 Достижения</div>
          <div style="font-size:12px;color:#C9A84C;margin-top:4px">${p.achievements && p.achievements.length > 0 ? p.achievements.length + ' достижений получено' : ''}</div>
          <div style="margin-top:8px">${p.achievements && p.achievements.length > 0 ? p.achievements.map(a => '<span class="badge" style="margin:3px">'+a.icon+' '+a.name+'</span>').join('') : '<div class="card-text">Выполняйте задания для получения наград!</div>'}</div>
        </div>
        <div class="card">
          <div class="card-title">🤝 Рефералы</div>
          ${p.referrals && Object.keys(p.referrals).length > 0 ? Object.entries(p.referrals).map(([k,v]) => '<div class="stat-row"><span class="stat-label">'+k.replace('_',' ')+'</span><span class="stat-val">'+v.count+' чел / '+v.caps_earned+' 🍺</span></div>').join('') : '<div class="card-text">Приглашайте друзей и получайте крышки!</div>'}
          <div style="margin-top:12px;padding:10px;background:rgba(212,135,28,.1);border-radius:8px;text-align:center">
            <div style="font-size:12px;color:#C9A84C;margin-bottom:4px">Ваша реф. ссылка:</div>
            <div style="font-size:11px;color:#FFF8E7;word-break:break-all;margin-bottom:8px">https://t.me/CRAFT_hell_bot?start=ref_${APP.tgId}</div>
            <button style="padding:6px 14px;background:linear-gradient(135deg,#D4871C,#C9A84C);border:none;border-radius:8px;color:#1A1209;font-size:11px;font-weight:600;cursor:pointer" onclick="copyRefLink('https://t.me/CRAFT_hell_bot?start=ref_${APP.tgId}')">📋 Копировать</button>
          </div>
        </div>`;
      APP.balance = p.caps_balance;
      updateBalance();
    } else {
      el.innerHTML = '<div class="card"><div class="card-text">Ошибка загрузки профиля</div></div>';
    }
  } catch(e) {
    el.innerHTML = '<div class="card"><div class="card-text">Ошибка соединения</div></div>';
  }
}

/* ============ CONNECTION / OFFERS ============ */
async function loadConnection() {
  const el = document.getElementById('connectionContent');
  try {
    const r = await api('/api/offers', null, 'GET');
    if (r.success && r.offers && r.offers.length > 0) {
      let offersHtml = '';
      const offerIcons = {checks_1_10k:'💳',checks_10k_plus:'🏦',sim:'📱',qr_nspk:'📲',bt:'🔒'};
      r.offers.forEach(o => {
        const icon = offerIcons[o.category] || '📌';
        const rateText = o.rate_from === o.rate_to ? o.rate_from + '%' : o.rate_from + '-' + o.rate_to + '%';
        offersHtml += '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(212,135,28,.15)">' +
          '<span style="font-size:14px;color:#C9A84C">' + icon + ' ' + o.description + '</span>' +
          '<span style="font-size:16px;font-weight:700;color:#FFF8E7">' + rateText + '</span></div>';
      });
      el.innerHTML = '<div class="card" style="border-color:rgba(212,175,55,.5);background:linear-gradient(135deg,rgba(42,30,18,.95),rgba(50,35,15,.95))">' +
        '<div style="text-align:center;margin-bottom:16px"><div style="font-size:42px;animation:beerGlow 2s ease-in-out infinite">🍺</div>' +
        '<div style="font-size:20px;font-weight:700;color:#D4871C;margin-top:8px">CRAFT - Geotransfer</div>' +
        '<div style="font-size:13px;color:#C9A84C;margin-top:4px">Подключение к площадке Geotransfer</div></div>' +
        '<div style="background:rgba(26,18,9,.6);border-radius:10px;padding:14px;margin-bottom:12px">' + offersHtml +
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(212,135,28,.15)">' +
        '<span style="font-size:14px;color:#C9A84C">🛡️ Страховой депозит</span><span style="font-size:16px;font-weight:700;color:#FFF8E7">500$</span></div>' +
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0">' +
        '<span style="font-size:14px;color:#C9A84C">💼 Рабочий депозит</span><span style="font-size:16px;font-weight:700;color:#FFF8E7">от 300$</span></div></div>' +
        '<button class="btn btn-primary" onclick="showScreen(\'appForm\')" style="animation:beerGlow 2s ease-in-out infinite">📋 Подать заявку</button></div>';
    }
  } catch(e) { console.error('Failed to load offers', e); }
}

/* ============ APPLICATION FORM (Step-by-step) ============ */
const APP_QUESTIONS = [
  "Как давно в сфере процессинга?",
  "Работаешь сейчас где-то? Если да, то где, по какому методу (Ферма/БТ/Залив и тд.)",
  "Почему ищешь другую площадку, чем не нравится та, где стоишь сейчас? (Если нигде не работаешь - ответь \"Не работаю\")",
  "Какой у тебя рабочий депозит?",
  "Сколько реквизитов у тебя есть сейчас на руках, сколько сможешь включить в работу в первую неделю работы? (Можешь ответить максимально подробно, кол-во/Банки)",
  "Почему мы должны взять тебя в свою команду?"
];
let appStep = 0;
let appAnswers = [];

function initAppForm() {
  appStep = 0; appAnswers = [];
  renderAppStep();
}
function renderAppStep() {
  document.getElementById('appStepLabel').textContent = (appStep+1) + '/6';
  document.getElementById('appProgress').style.width = ((appStep+1)/6*100) + '%';
  document.getElementById('appQuestionTitle').textContent = 'Вопрос ' + (appStep+1) + ' из 6';
  document.getElementById('appQuestionText').textContent = APP_QUESTIONS[appStep];
  document.getElementById('appAnswer').value = appAnswers[appStep] || '';
  document.getElementById('appAnswer').placeholder = 'Ваш ответ...';
  const btn = document.getElementById('appNextBtn');
  btn.textContent = appStep === 5 ? '📨 Отправить заявку' : 'Далее →';
  btn.disabled = false;
}
function appFormBack() {
  if (appStep > 0) { appStep--; renderAppStep(); }
  else { showScreen('connection'); }
}
function appFormNext() {
  const answer = document.getElementById('appAnswer').value.trim();
  if (!answer) { toast('Напишите ответ на вопрос'); return; }
  appAnswers[appStep] = answer;
  if (appStep < 5) { appStep++; renderAppStep(); }
  else { submitApplication(); }
}
async function submitApplication() {
  const btn = document.getElementById('appNextBtn');
  btn.disabled = true; btn.textContent = '⏳ Отправка...';
  const form_data = {};
  APP_QUESTIONS.forEach((q, i) => { form_data['q'+(i+1)] = q; form_data['a'+(i+1)] = appAnswers[i]; });
  try {
    const r = await api('/api/application/submit', { telegram_id: APP.tgId, form_data });
    if (r.success) {
      toast('✅ Заявка отправлена!');
      setTimeout(() => showScreen('main'), 1500);
    } else { toast('❌ ' + (r.error || 'Ошибка')); }
  } catch(e) { toast('❌ Ошибка соединения'); }
  btn.disabled = false; btn.textContent = '📨 Отправить заявку';
}

/* ============ SOS ============ */
async function submitSOS() {
  const btn = document.getElementById('sosSubmitBtn');
  const city = document.getElementById('sosCity').value.trim();
  const contact = document.getElementById('sosContact').value.trim();
  const desc = document.getElementById('sosDesc').value.trim();
  
  if (!city || !contact || !desc) { toast('Заполните все поля'); return; }
  
  btn.disabled = true; btn.textContent = '⏳ Отправка...';
  try {
    const r = await api('/api/sos/submit', { telegram_id: APP.tgId, city, contact, description: desc });
    if (r.success) {
      toast('✅ SOS заявка отправлена! Ожидайте ответа');
      setTimeout(() => showScreen('main'), 1500);
    } else {
      toast('❌ ' + (r.error || 'Ошибка'));
    }
  } catch(e) { toast('❌ Ошибка соединения'); }
  btn.disabled = false; btn.textContent = '🆘 Отправить SOS';
}

/* ============ SUPPORT ============ */
async function submitSupport() {
  const btn = document.getElementById('supportBtn');
  const msg = document.getElementById('supportMsg').value.trim();
  if (!msg) { toast('Напишите сообщение'); return; }
  
  btn.disabled = true; btn.textContent = '⏳ Отправка...';
  try {
    const r = await api('/api/support/submit', { telegram_id: APP.tgId, message: msg });
    if (r.success) {
      toast('✅ Обращение отправлено!');
      document.getElementById('supportMsg').value = '';
      setTimeout(() => showScreen('main'), 1500);
    } else { toast('❌ ' + (r.error || 'Ошибка')); }
  } catch(e) { toast('❌ Ошибка соединения'); }
  btn.disabled = false; btn.textContent = '📨 Отправить';
}

/* ============ AI CHAT ============ */
let chatBusy = false;
async function sendChat() {
  if (chatBusy) return;
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;
  
  input.value = '';
  addChatMsg(msg, 'user');
  chatBusy = true;
  
  const typingEl = addChatMsg('Михалыч печатает...', 'bot');
  
  try {
    const r = await api('/api/ai/chat', { telegram_id: APP.tgId, message: msg });
    typingEl.remove();
    if (r.success) {
      addChatMsg(r.response, 'bot');
      APP.balance = Math.max(0, APP.balance - (r.caps_spent !== undefined ? r.caps_spent : 5));
      updateBalance();
    } else {
      addChatMsg('❌ ' + (r.error || 'Ошибка'), 'bot');
    }
  } catch(e) {
    typingEl.remove();
    addChatMsg('❌ Ошибка соединения', 'bot');
  }
  chatBusy = false;
}
function addChatMsg(text, type) {
  const el = document.createElement('div');
  el.className = 'chat-msg ' + type;
  if (type === 'bot') {
    let html = text.replace(/\n/g, '<br>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
    html = html.replace(/^▸ /gm, '▸ ');
    html = html.replace(/^- /gm, '▸ ');
    el.innerHTML = html;
  } else {
    el.textContent = text;
  }
  const container = document.getElementById('chatMessages');
  container.appendChild(el);
  container.scrollTop = container.scrollHeight;
  return el;
}

/* ============ UNIVERSITY ============ */
let universityLessons = [];
async function loadUniversity() {
  const el = document.getElementById('universityContent');
  el.innerHTML = '<div class="loader"></div>';
  try {
    const r = await api('/api/university/lessons', null, 'GET');
    if (r.success && r.lessons) {
      universityLessons = r.lessons;
      let html = '<div class="card" style="margin-bottom:16px"><div class="card-title">🏫 Университет CRAFT</div><div class="card-text">Изучайте уроки, сдавайте экзамены и зарабатывайте крышки!</div></div>';
      r.lessons.forEach((l, i) => {
        html += `<div class="lesson-card" onclick="openLesson(${i})" style="${l.completed ? 'border-color:rgba(46,125,50,.5)' : ''}">
          <div class="lesson-num">${l.completed ? '✅ ' : ''}Урок ${l.order_index || i+1}</div>
          <div class="lesson-title">${l.title}</div>
          <div class="lesson-reward">${l.completed ? 'Пройден ✓' : 'Награда: ' + l.reward_caps + ' 🍺'}</div>
        </div>`;
      });
      el.innerHTML = html;
    } else {
      el.innerHTML = '<div class="card"><div class="card-text">Уроки скоро появятся</div></div>';
    }
  } catch(e) { el.innerHTML = '<div class="card"><div class="card-text">Ошибка загрузки</div></div>'; }
}
function openLesson(idx) {
  const l = universityLessons[idx];
  if (!l) return;
  const el = document.getElementById('universityContent');
  let quiz = [];
  try { quiz = JSON.parse(l.exam_questions || '[]'); } catch(e) {}
  let html = '<div class="card"><div style="display:flex;align-items:center;gap:10px;margin-bottom:14px"><button class="back-btn" onclick="loadUniversity()">←</button><div class="card-title" style="margin:0">📖 ' + l.title + '</div></div>' +
    '<div class="lesson-content">' + l.content.replace(/\n/g, '<br>') + '</div></div>';
  if (quiz.length > 0) {
    html += '<div class="card" style="text-align:center"><button class="exam-start-btn" onclick="startExam(' + idx + ')">🎓 Начать экзамен</button></div>';
  }
  el.innerHTML = html;
}
var examState = null;
function startExam(idx) {
  const l = universityLessons[idx];
  let quiz = [];
  try { quiz = JSON.parse(l.exam_questions || '[]'); } catch(e) {}
  if (!quiz.length) return;
  examState = {lessonIdx: idx, lessonId: l.id, quiz: quiz, current: 0, correct: 0, answers: {}};
  showExamQuestion();
}
function showExamQuestion() {
  if (!examState) return;
  const s = examState, q = s.quiz[s.current], total = s.quiz.length, num = s.current + 1;
  const el = document.getElementById('universityContent');
  const pct = Math.round((s.current / total) * 100);
  let html = '<div class="card exam-slide">' +
    '<div class="exam-progress-bar"><div class="exam-progress-fill" style="width:' + pct + '%"></div></div>' +
    '<div class="exam-question-num">Вопрос ' + num + ' из ' + total + '</div>' +
    '<div class="quiz-question">' + (q.q || q.question) + '</div>';
  q.options.forEach(function(opt, oi) {
    html += '<div class="quiz-option" id="eq' + s.current + 'o' + oi + '" onclick="examAnswer(' + oi + ',' + q.correct + ')">' + opt + '</div>';
  });
  html += '</div>';
  el.innerHTML = html;
}
function examAnswer(oi, correct) {
  if (!examState || examState.answers[examState.current] !== undefined) return;
  var s = examState;
  s.answers[s.current] = oi;
  var opts = document.querySelectorAll('[id^="eq' + s.current + 'o"]');
  opts.forEach(function(o, i) {
    o.style.pointerEvents = 'none';
    if (i === correct) { o.classList.add('correct'); o.style.transition = 'all .3s ease'; }
    else if (i === oi) { o.classList.add('wrong'); o.style.transition = 'all .3s ease'; }
  });
  if (oi === correct) s.correct++;
  setTimeout(function() {
    s.current++;
    if (s.current < s.quiz.length) { showExamQuestion(); }
    else { showExamResult(); }
  }, 1000);
}
async function showExamResult() {
  var s = examState, total = s.quiz.length, score = s.correct;
  var perfect = score === total;
  
  if (perfect) {
    /* Сразу отправляем на сервер */
    var r = await api('/api/university/complete', {telegram_id: APP.tgId, lesson_id: s.lessonId, score: score, total: total});
    var reward = (r && r.reward) || 0;
    var alreadyDone = r && r.already_completed;
    launchConfetti();
    
    /* Fullscreen overlay */
    var overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at center,rgba(30,20,10,.97) 0%,rgba(10,6,3,.99) 100%);display:flex;align-items:center;justify-content:center;z-index:9998;opacity:0;transition:opacity .4s ease';
    overlay.innerHTML = '<div style="text-align:center;transform:scale(.8);opacity:0;transition:all .5s cubic-bezier(.34,1.56,.64,1);max-width:320px;padding:0 20px" id="examResultInner">' +
      '<div style="position:relative;width:120px;height:120px;margin:0 auto 24px">' +
        '<div style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,#D4871C,#F4C430,#FFD700,#D4871C);animation:spin 3s linear infinite;opacity:.3;filter:blur(15px)"></div>' +
        '<div style="position:absolute;inset:8px;border-radius:50%;background:radial-gradient(circle,rgba(42,30,18,.9),rgba(26,14,10,.95));display:flex;align-items:center;justify-content:center;border:2px solid rgba(244,196,48,.4)">' +
          '<span style="font-size:48px;filter:drop-shadow(0 0 20px rgba(244,196,48,.5))">🎓</span>' +
        '</div>' +
      '</div>' +
      '<div style="font-size:28px;font-weight:800;background:linear-gradient(135deg,#F4C430,#FFD700,#D4871C);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;letter-spacing:-.5px">Экзамен сдан!</div>' +
      '<div style="font-size:15px;color:rgba(255,248,231,.7);margin-bottom:24px">' + score + ' из ' + total + ' — безупречно</div>' +
      (alreadyDone ? '<div style="font-size:13px;color:rgba(201,168,76,.6);margin-bottom:16px">Урок был пройден ранее</div>' : 
        '<div style="display:inline-flex;align-items:center;gap:8px;padding:12px 24px;background:rgba(244,196,48,.1);border:1px solid rgba(244,196,48,.2);border-radius:20px;margin-bottom:24px">' +
          '<span style="font-size:22px">🍺</span>' +
          '<span style="font-size:20px;font-weight:700;color:#F4C430">+' + reward + '</span>' +
          '<span style="font-size:14px;color:rgba(255,248,231,.6)">крышек</span>' +
        '</div>') +
      '<div><button onclick="this.closest(\'div[style*=fixed]\').remove();loadUniversity()" style="width:100%;padding:16px 32px;background:linear-gradient(135deg,#D4871C 0%,#F4C430 50%,#D4871C 100%);background-size:200% auto;animation:shimmer 2s linear infinite;border:none;border-radius:16px;color:#1A0E0A;font-weight:700;font-size:16px;cursor:pointer;letter-spacing:.3px;box-shadow:0 4px 20px rgba(212,135,28,.4)">Продолжить</button></div>' +
    '</div>';
    document.body.appendChild(overlay);
    requestAnimationFrame(function(){
      overlay.style.opacity = '1';
      setTimeout(function(){
        var inner = document.getElementById('examResultInner');
        if (inner) { inner.style.transform = 'scale(1)'; inner.style.opacity = '1'; }
      }, 100);
    });
    if (reward > 0) { APP.balance += reward; updateBalance(); }
  } else {
    /* Не все верные — показываем в контенте */
    var el = document.getElementById('universityContent');
    el.innerHTML = '<div class="card exam-slide" style="text-align:center;padding:40px 20px">' +
      '<div style="position:relative;width:100px;height:100px;margin:0 auto 20px">' +
        '<div style="position:absolute;inset:0;border-radius:50%;background:rgba(198,40,40,.15);border:2px solid rgba(198,40,40,.3);display:flex;align-items:center;justify-content:center">' +
          '<span style="font-size:44px">📝</span>' +
        '</div>' +
      '</div>' +
      '<div style="font-size:22px;font-weight:700;color:#C9A84C;margin-bottom:6px">' + score + ' из ' + total + '</div>' +
      '<div style="font-size:14px;color:rgba(255,248,231,.5);margin-bottom:28px">Нужно ответить на все вопросы правильно</div>' +
      '<button class="exam-start-btn" onclick="startExam(' + s.lessonIdx + ')" style="margin-bottom:10px;background:linear-gradient(135deg,#8B6914,#C9A84C)">🔄 Попробовать снова</button>' +
      '<button style="display:block;width:100%;padding:14px;background:transparent;border:1px solid rgba(212,135,28,.15);border-radius:14px;color:rgba(201,168,76,.5);font-size:14px;cursor:pointer" onclick="loadUniversity()">← К урокам</button>' +
    '</div>';
  }
}
function launchConfetti() {
  var colors = ['#F4C430','#D4871C','#FFD700','#FF6B35','#4CAF50','#E91E63','#9C27B0','#00BCD4'];
  for (var i = 0; i < 60; i++) {
    var piece = document.createElement('div');
    piece.className = 'confetti-piece';
    piece.style.left = Math.random() * 100 + 'vw';
    piece.style.background = colors[Math.floor(Math.random() * colors.length)];
    piece.style.animationDuration = (2.5 + Math.random() * 2.5) + 's';
    piece.style.animationDelay = Math.random() * 1 + 's';
    var size = 5 + Math.random() * 10;
    piece.style.width = size + 'px';
    piece.style.height = size * (0.4 + Math.random() * 0.6) + 'px';
    piece.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
    document.body.appendChild(piece);
    setTimeout(function(p){ p.remove(); }, 6000, piece);
  }
}

/* ============ REFERRAL ============ */
async function loadReferral() {
  const el = document.getElementById('referralContent');
  el.innerHTML = '<div class="loader"></div>';
  try {
    const r = await api('/api/referral/stats?telegram_id=' + APP.tgId, null, 'GET');
    if (r.success) {
      const s = r.stats;
      el.innerHTML = `
        <div class="card">
          <div class="card-title">🤝 Реферальная программа</div>
          <div class="card-text" style="margin-bottom:12px">Приглашайте друзей — получайте крышки!</div>
          <div class="stat-row"><span class="stat-label">👥 Рефералов 1-й уровень</span><span class="stat-val">${s.level1_count} чел</span></div>
          <div class="stat-row"><span class="stat-label">👥 Рефералов 2-й уровень</span><span class="stat-val">${s.level2_count} чел</span></div>
          <div class="stat-row"><span class="stat-label">💰 Всего заработано</span><span class="stat-val">${s.total_earned} 🍺</span></div>
          <div class="stat-row"><span class="stat-label">Уровень 1</span><span class="stat-val">5% + 30 🍺</span></div>
          <div class="stat-row"><span class="stat-label">Уровень 2</span><span class="stat-val">2% + 15 🍺</span></div>
        </div>
        ${s.recent && s.recent.length > 0 ? '<div class="card"><div class="card-title">🕐 Последние рефералы</div>' + s.recent.map(r => '<div class="ref-recent"><span class="ref-recent-name">' + r.name + '</span> <span class="ref-recent-date">' + r.date + '</span></div>').join('') + '</div>' : ''}
        <div class="card">
          <div class="card-title">🔗 Ваша ссылка</div>
          <div style="padding:12px;background:rgba(26,18,9,.8);border-radius:8px;margin-top:8px;font-size:12px;color:#FFF8E7;word-break:break-all;text-align:center">
            https://t.me/CRAFT_hell_bot?start=ref_${APP.tgId}
          </div>
          <button class="btn btn-primary" style="margin-top:10px;font-size:13px;padding:10px" onclick="copyRefLink('https://t.me/CRAFT_hell_bot?start=ref_${APP.tgId}')">📋 Копировать ссылку</button>
        </div>`;
    } else { throw new Error(); }
  } catch(e) {
    if (!APP.profile) { await loadCabinet(); }
    const p = APP.profile || {};
    const refs = p.referrals || {};
    const l1 = refs.level_1 || {count:0,caps_earned:0};
    const l2 = refs.level_2 || {count:0,caps_earned:0};
    el.innerHTML = `
      <div class="card">
        <div class="card-title">🤝 Реферальная программа</div>
        <div class="stat-row"><span class="stat-label">👥 1-й уровень</span><span class="stat-val">${l1.count} чел / ${l1.caps_earned} 🍺</span></div>
        <div class="stat-row"><span class="stat-label">👥 2-й уровень</span><span class="stat-val">${l2.count} чел / ${l2.caps_earned} 🍺</span></div>
      </div>
      <div class="card">
        <div class="card-title">🔗 Ваша ссылка</div>
        <div style="padding:12px;background:rgba(26,18,9,.8);border-radius:8px;margin-top:8px;font-size:12px;color:#FFF8E7;word-break:break-all;text-align:center">
          https://t.me/CRAFT_hell_bot?start=ref_${APP.tgId}
        </div>
        <button class="btn btn-primary" style="margin-top:10px;font-size:13px;padding:10px" onclick="copyRefLink('https://t.me/CRAFT_hell_bot?start=ref_${APP.tgId}')">📋 Копировать ссылку</button>
      </div>`;
  }
}

/* ============ ACHIEVEMENTS ============ */
async function loadAchievements() {
  const el = document.getElementById('achievementsContent');
  el.innerHTML = '<div class="loader"></div>';
  try {
    const r = await api('/api/achievements/all?telegram_id=' + APP.tgId, null, 'GET');
    if (r.success) {
      const all = r.achievements;
      const earned = all.filter(function(a){return a.earned});
      const locked = all.filter(function(a){return !a.earned});
      var achHtml = '<div class="card" style="margin-bottom:12px"><div class="card-title">🏆 Достижения</div><div class="card-text">Получено: ' + earned.length + '/' + all.length + '</div></div>';
      if (earned.length > 0) {
        achHtml += '<div class="achievements-section-title">✅ Получено</div>';
        achHtml += earned.map(function(a){return '<div class="card achievement-unlocked"><div style="display:flex;align-items:center;gap:12px"><div style="font-size:32px">' + a.icon + '</div><div><div style="font-weight:600;color:#FFF8E7">' + a.name + '</div><div style="font-size:12px;color:#C9A84C">' + a.description + '</div><div style="font-size:11px;color:#4CAF50;margin-top:2px">+' + a.reward_caps + ' 🍺 ✅</div></div></div></div>'}).join('');
      }
      if (locked.length > 0) {
        achHtml += '<div class="achievements-section-title">🔒 Доступно</div>';
        achHtml += locked.map(function(a){return '<div class="card achievement-locked"><div style="display:flex;align-items:center;gap:12px"><div style="font-size:32px">' + a.icon + '</div><div><div style="font-weight:600;color:#FFF8E7">' + a.name + '</div><div style="font-size:12px;color:#C9A84C">' + a.description + '</div><div style="font-size:11px;color:#D4871C;margin-top:2px">+' + a.reward_caps + ' 🍺 🔒</div></div></div></div>'}).join('');
      }
      el.innerHTML = achHtml;
    } else { throw new Error(); }
  } catch(e) {
    if (!APP.profile) await loadCabinet();
    const achs = (APP.profile && APP.profile.achievements) || [];
    el.innerHTML = achs.length > 0 ? achs.map(a => `<div class="card achievement-unlocked"><div style="display:flex;align-items:center;gap:12px"><div style="font-size:32px">${a.icon}</div><div><div style="font-weight:600;color:#FFF8E7">${a.name}</div><div style="font-size:12px;color:#C9A84C">+${a.reward_caps} 🍺 ✅</div></div></div></div>`).join('') : '<div class="card"><div class="card-text">Выполняйте задания для получения наград!</div></div>';
  }
}

/* ============ UTILS ============ */
async function api(url, body, method) {
  method = method || (body ? 'POST' : 'GET');
  const initData = (tg && tg.initData) ? tg.initData : '';
  if (method === 'GET' && initData) {
    url += (url.includes('?') ? '&' : '?') + 'init_data=' + encodeURIComponent(initData);
  }
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body && method !== 'GET') {
    if (initData) body.init_data = initData;
    opts.body = JSON.stringify(body);
  }
  const r = await fetch(API + url, opts);
  return r.json();
}
function show(id) { document.getElementById(id).style.display = 'flex'; }
function hide(id) { document.getElementById(id).style.display = 'none'; }
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg; el.style.display = 'block';
  setTimeout(() => { el.style.display = 'none'; }, 2500);
}
/* ============ CLIPBOARD ============ */
function copyRefLink(link) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(link).then(() => toast('✅ Ссылка скопирована!')).catch(() => fallbackCopy(link));
  } else { fallbackCopy(link); }
}
function fallbackCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); toast('✅ Ссылка скопирована!'); } catch(e) { toast('📋 Скопируйте вручную'); }
  document.body.removeChild(ta);
}
/* ============ BEER BUBBLES — БЛЕСТЯЩИЕ ============ */
function createBubbles() {
  const container = document.getElementById('bubbles');
  if (!container) return;
  for (let i = 0; i < 15; i++) {
    const b = document.createElement('div');
    b.className = 'bubble';
    const size = Math.random() * 25 + 8;
    b.style.width = size + 'px';
    b.style.height = size + 'px';
    b.style.left = (Math.random() * 90 + 5) + '%';
    const riseDur = Math.random() * 8 + 7;
    const sparkleDur = Math.random() * 1.5 + 1.5;
    const wobbleDur = Math.random() * 2 + 2;
    b.style.animationDuration = riseDur+'s,'+sparkleDur+'s,'+wobbleDur+'s';
    b.style.animationDelay = (Math.random() * 15) + 's,'+(Math.random()*2)+'s,'+(Math.random()*2)+'s';
    // Vary brightness per bubble
    const hue = Math.random() * 20 + 35; // 35-55 gold range
    const lightness = Math.random() * 20 + 50;
    b.style.setProperty('--glow-color', 'hsl('+hue+',80%,'+lightness+'%)');
    container.appendChild(b);
  }
  // Create a few extra large "champagne" bubbles
  for (let i = 0; i < 3; i++) {
    const b = document.createElement('div');
    b.className = 'bubble';
    const size = Math.random() * 12 + 22;
    b.style.width = size + 'px';
    b.style.height = size + 'px';
    b.style.left = (Math.random() * 80 + 10) + '%';
    b.style.animationDuration = (Math.random()*6+10)+'s,2.5s,3.5s';
    b.style.animationDelay = (Math.random()*20)+'s,0s,0s';
    b.style.opacity = '0.5';
    container.appendChild(b);
  }
}
createBubbles();

/* ============ NEWS ============ */
async function loadNews() {
  const el = document.getElementById('newsContent');
  el.innerHTML = '<div class="loader"></div>';
  try {
    const r = await api('/api/news/status?telegram_id=' + APP.tgId, null, 'GET');
    if (r.success) {
      const isSub = r.is_subscribed;
      const cost = r.daily_cost || 10;
      let expiresText = '';
      if (isSub && r.expires_at) {
        const d = new Date(r.expires_at);
        expiresText = d.toLocaleDateString('ru-RU', {day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'});
      }
      el.innerHTML = '<div class="card">' +
        '<div style="text-align:center;margin-bottom:16px">' +
        '<div style="font-size:48px">📰</div>' +
        '<div style="font-size:20px;font-weight:700;color:#D4871C;margin-top:8px">CRAFT Daily</div>' +
        '<div style="font-size:13px;color:#C9A84C;margin-top:4px">Ежедневный дайджест рынка процессинга</div></div>' +
        '<div style="padding:12px;margin-bottom:12px;border-radius:10px;background:rgba(212,135,28,0.08);border:1px solid rgba(212,135,28,0.15)">' +
        '<div style="font-size:13px;color:#C9A84C;line-height:1.6">' +
        '📊 <b>Рынок и ставки</b> — актуальные % и тренды<br>' +
        '🛠 <b>Методы</b> — рабочие схемы и мануалы<br>' +
        '⚠️ <b>Безопасность</b> — блокировки, ФЗ, кейсы<br>' +
        '💡 <b>Полезное</b> — лайфхаки и инструменты<br><br>' +
        'Сводка из <b>50+ профильных ТГ-каналов</b> каждое утро в 10:00 МСК прямо в личку от бота.</div></div>' +
        '<div class="stat-row"><span class="stat-label">Статус</span><span class="stat-val" style="color:' + (isSub ? '#4CAF50' : '#ff6b6b') + '">' + (isSub ? '✅ Активна' : '❌ Неактивна') + '</span></div>' +
        '<div class="stat-row"><span class="stat-label">Стоимость</span><span class="stat-val">' + (APP.userLevel === 'vip' ? '👑 Бесплатно (VIP)' : cost + ' 🍺 / день') + '</span></div>' +
        '<div style="margin-top:16px">' +
        (isSub ?
          '<button class="btn btn-danger" onclick="newsUnsubscribe()">❌ Отписаться</button>'
          :
          '<button class="btn btn-primary" onclick="newsSubscribe()">📰 Подписаться' + (APP.userLevel === 'vip' ? ' (бесплатно)' : ' (' + cost + ' 🍺/день)') + '</button>'
        ) +
        '</div></div>';
    } else { throw new Error(); }
  } catch(e) { el.innerHTML = '<div class="card"><div class="card-text">Ошибка загрузки</div></div>'; }
}
async function newsSubscribe() {
  try {
    const r = await api('/api/news/subscribe', {telegram_id: APP.tgId});
    if (r.success) { APP.balance = r.new_balance; updateBalance(); toast('✅ Подписка оформлена!'); loadNews(); }
    else { toast('❌ ' + (r.error || 'Ошибка')); }
  } catch(e) { toast('❌ Ошибка соединения'); }
}
async function newsUnsubscribe() {
  try {
    const r = await api('/api/news/unsubscribe', {telegram_id: APP.tgId});
    if (r.success) { toast('✅ Подписка отменена'); loadNews(); }
    else { toast('❌ ' + (r.error || 'Ошибка')); }
  } catch(e) { toast('❌ Ошибка соединения'); }
}
/* ============ SHOP ============ */
let shopAllItems = {};
let shopCart = [];
let shopFilter = 'all';

async function loadShopItems() {
  const el = document.getElementById('shopItems');
  el.innerHTML = '<div class="loader"></div>';
  try {
    const r = await api('/api/shop/items');
    if (r.success) {
      shopAllItems = r.items;
      renderShopItems();
      updateCartBadge();
    }
  } catch(e) { el.innerHTML = '<div class="card-text">Ошибка загрузки</div>'; }
}

function renderShopItems() {
  const el = document.getElementById('shopItems');
  let html = '';
  const cats = shopFilter === 'all' ? Object.keys(shopAllItems) : [shopFilter];
  cats.forEach(cat => {
    const items = shopAllItems[cat];
    if (!items) return;
    items.forEach(item => {
      const inCart = shopCart.includes(item.id);
      html += '<div class="card" style="border-color:rgba(212,135,28,.3);padding:14px">' +
        '<div style="display:flex;justify-content:space-between;align-items:center">' +
        '<div><div style="font-size:15px;font-weight:700;color:#FFF8E7">' + item.title + (item.file_type ? ' <span style="font-size:10px;color:#888;background:rgba(212,135,28,.15);padding:2px 6px;border-radius:4px;margin-left:4px">' + item.file_type.toUpperCase() + '</span>' : '') + '</div>' +
        '<div style="font-size:12px;color:#C9A84C;margin-top:4px">' + (item.description||'') + '</div></div>' +
        '<div style="text-align:right;min-width:80px"><div style="font-size:16px;font-weight:700;color:#F4C430">' + item.price_caps + ' 🍺</div>' +
        '<button onclick="toggleCart(' + item.id + ')" style="margin-top:6px;padding:5px 12px;border-radius:8px;border:1px solid ' +
        (inCart ? 'rgba(220,60,60,.6);background:rgba(220,60,60,.15);color:#ff6b6b' : 'rgba(212,135,28,.4);background:rgba(212,135,28,.15);color:#F4C430') +
        ';font-size:11px;cursor:pointer;font-weight:600">' + (inCart ? '✕ Убрать' : '+ В корзину') + '</button></div></div></div>';
    });
  });
  if (!html) html = '<div class="card-text" style="text-align:center;color:#C9A84C">Нет товаров</div>';
  el.innerHTML = html;
}

function filterShop(cat, btn) {
  shopFilter = cat;
  document.querySelectorAll('.shop-tab').forEach(t => {
    t.style.background = 'transparent';
    t.style.color = '#C9A84C';
    t.classList.remove('active');
  });
  btn.style.background = 'rgba(212,135,28,.2)';
  btn.style.color = '#F4C430';
  btn.classList.add('active');
  renderShopItems();
}

async function toggleCart(itemId) {
  const inCart = shopCart.includes(itemId);
  try {
    const r = await api(inCart ? '/api/shop/cart/remove' : '/api/shop/cart/add', {item_id: itemId});
    if (r.success) {
      if (inCart) shopCart = shopCart.filter(i => i !== itemId);
      else shopCart.push(itemId);
      renderShopItems();
      updateCartBadge();
      toast(inCart ? '✕ Убрано из корзины' : '✅ Добавлено в корзину');
    } else {
      toast('❌ ' + (r.error || 'Ошибка'));
    }
  } catch(e) { toast('❌ Ошибка: ' + e.message); }
}

function updateCartBadge() {
  const badge = document.getElementById('cartCount');
  if (shopCart.length > 0) {
    badge.textContent = shopCart.length;
    badge.style.display = 'inline';
  } else {
    badge.style.display = 'none';
  }
}

function showShopCart() { showScreen('cart'); }

async function loadShopCart() {
  const el = document.getElementById('cartItems');
  el.innerHTML = '<div class="loader"></div>';
  try {
    const r = await api('/api/shop/cart');
    if (r.success) {
      shopCart = r.items.map(i => i.id);
      let html = '';
      r.items.forEach(item => {
        html += '<div class="card" style="border-color:rgba(212,135,28,.3);padding:12px;display:flex;justify-content:space-between;align-items:center">' +
          '<div><div style="font-size:14px;font-weight:600;color:#FFF8E7">' + item.title + '</div>' +
          '<div style="font-size:12px;color:#C9A84C">' + item.price_caps + ' 🍺</div></div>' +
          '<button onclick="removeFromCart(' + item.id + ')" style="padding:4px 10px;border-radius:8px;border:1px solid rgba(220,60,60,.4);background:rgba(220,60,60,.1);color:#ff6b6b;font-size:11px;cursor:pointer">✕</button></div>';
      });
      if (!html) html = '<div class="card-text" style="text-align:center;color:#C9A84C">Корзина пуста</div>';
      el.innerHTML = html;
      document.getElementById('cartTotal').textContent = r.total > 0 ? 'Итого: ' + r.total + ' 🍺' : '';
      document.getElementById('checkoutBtn').style.display = r.items.length > 0 ? 'block' : 'none';
    }
  } catch(e) { el.innerHTML = '<div class="card-text">Ошибка</div>'; }
}

async function removeFromCart(itemId) {
  try {
    const r = await api('/api/shop/cart/remove', {item_id: itemId});
    if (r.success) { shopCart = shopCart.filter(i => i !== itemId); loadShopCart(); updateCartBadge(); }
  } catch(e) { toast('Ошибка', 'error'); }
}

async function shopCheckout() {
  const btn = document.getElementById('checkoutBtn');
  btn.disabled = true; btn.textContent = '⏳ Обработка...';
  try {
    const r = await api('/api/shop/checkout', {});
    if (r.success) {
      APP.balance = r.new_balance;
      updateBalance();
      toast('✅ Покупка совершена! Списано ' + r.total_spent + ' крышек');
      shopCart = [];
      updateCartBadge();
      loadShopCart();
    } else {
      toast('❌ ' + (r.error || 'Ошибка покупки'));
    }
  } catch(e) { toast('Ошибка', 'error'); }
  btn.disabled = false; btn.textContent = '💰 Купить';
}
</script>
<!-- ===== PURCHASE HISTORY ===== -->
<div class="overlay" id="screenPurchaseHistory">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('shop')">←</button>
      <div class="sub-title">📋 История покупок</div>
    </div>
    <div class="content fade-in" id="purchaseHistoryContent">
      <div class="loader"></div>
    </div>
  </div>
</div>

<!-- ===== BALANCE HISTORY ===== -->
<div class="overlay" id="screenBalanceHistory">
  <div class="overlay-bg">
    <div class="sub-header">
      <button class="back-btn" onclick="showScreen('cabinet')">←</button>
      <div class="sub-title">📊 История баланса</div>
    </div>
    <div class="content fade-in">
      <div style="display:flex;gap:6px;margin-bottom:14px">
        <button class="shop-tab active" onclick="loadBalanceHistory('all',this)" style="padding:6px 12px;border-radius:20px;border:1px solid rgba(212,135,28,.4);background:rgba(212,135,28,.2);color:#F4C430;font-size:12px;cursor:pointer;font-weight:600">Все</button>
        <button class="shop-tab" onclick="loadBalanceHistory('income',this)" style="padding:6px 12px;border-radius:20px;border:1px solid rgba(212,135,28,.2);background:transparent;color:#C9A84C;font-size:12px;cursor:pointer">Начисления</button>
        <button class="shop-tab" onclick="loadBalanceHistory('expense',this)" style="padding:6px 12px;border-radius:20px;border:1px solid rgba(212,135,28,.2);background:transparent;color:#C9A84C;font-size:12px;cursor:pointer">Траты</button>
      </div>
      <div id="balanceHistoryContent"><div class="loader"></div></div>
    </div>
  </div>
</div>

<script>
async function loadPurchaseHistory() {
  const el = document.getElementById('purchaseHistoryContent');
  el.innerHTML = '<div class="loader"></div>';
  try {
    const r = await api('/api/shop/purchases', null, 'GET');
    if (r.success && r.purchases && r.purchases.length > 0) {
      let html = '';
      r.purchases.forEach(p => {
        const date = new Date(p.purchased_at).toLocaleDateString('ru-RU');
        html += '<div class="card" style="padding:12px">' +
          '<div style="display:flex;justify-content:space-between;align-items:center">' +
          '<div><div style="font-size:14px;font-weight:600;color:#FFF8E7">' + p.title + '</div>' +
          '<div style="font-size:11px;color:#C9A84C">' + p.category + ' • ' + date + '</div></div>' +
          '<div style="font-size:14px;font-weight:700;color:#F4C430">-' + p.price_paid + ' 🍺</div></div></div>';
      });
      el.innerHTML = html;
    } else {
      el.innerHTML = '<div class="card"><div class="card-text" style="text-align:center">Покупок пока нет</div></div>';
    }
  } catch(e) { el.innerHTML = '<div class="card-text">Ошибка загрузки</div>'; }
}

async function loadBalanceHistory(filter, btn) {
  filter = filter || 'all';
  if (btn) {
    document.querySelectorAll('#screenBalanceHistory .shop-tab').forEach(t => {
      t.style.background = 'transparent'; t.style.color = '#C9A84C';
    });
    btn.style.background = 'rgba(212,135,28,.2)'; btn.style.color = '#F4C430';
  }
  const el = document.getElementById('balanceHistoryContent');
  el.innerHTML = '<div class="loader"></div>';
  try {
    const r = await api('/api/balance/history?filter=' + filter, null, 'GET');
    if (r.success && r.history && r.history.length > 0) {
      let html = '';
      r.history.forEach(h => {
        const date = new Date(h.created_at).toLocaleDateString('ru-RU', {day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'});
        const isPositive = h.amount > 0;
        const color = isPositive ? '#4CAF50' : '#ff6b6b';
        const sign = isPositive ? '+' : '';
        const icon = h.operation === 'shop_purchase' ? '🛒' : h.operation === 'referral_bonus' ? '🤝' : h.operation === 'lesson_reward' ? '🎓' : h.operation === 'ai_cost' ? '🤖' : h.operation === 'registration_bonus' ? '🎁' : '💰';
        html += '<div class="card" style="padding:12px;margin-bottom:8px">' +
          '<div style="display:flex;justify-content:space-between;align-items:center">' +
          '<div><div style="font-size:13px;color:#FFF8E7">' + icon + ' ' + (h.description || h.operation) + '</div>' +
          '<div style="font-size:11px;color:#C9A84C">' + date + '</div></div>' +
          '<div style="text-align:right"><div style="font-size:15px;font-weight:700;color:' + color + '">' + sign + h.amount + ' 🍺</div>' +
          '<div style="font-size:10px;color:#888">Баланс: ' + (h.balance_after || '?') + '</div></div></div></div>';
      });
      el.innerHTML = html;
    } else {
      el.innerHTML = '<div class="card"><div class="card-text" style="text-align:center">Операций пока нет</div></div>';
    }
  } catch(e) { el.innerHTML = '<div class="card-text">Ошибка загрузки</div>'; }
}
</script>
</body>
</html>"""


@frontend_bp.route('/')
def home():
    resp = Response(MAIN_HTML, mimetype='text/html')
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    resp.headers['X-Build'] = '20260224-1400'
    return resp
