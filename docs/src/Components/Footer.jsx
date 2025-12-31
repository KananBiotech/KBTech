import React from 'react';

import { FaLocationDot, FaPhone, FaEnvelope, FaFacebook, FaTwitter, FaLinkedin, FaInstagram } from 'react-icons/fa6';

const Footer = () => {
    const { t } = useLanguage();
    
    return (
        <footer className="footer-container">
            <div className="footer-content">
                
                {/* Column 1: Logo & About */}
                <div className="footer-column">
                    <div className="footer-logo">{t('logo')}</div>
                    <p>
                        {t('footer_tagline')}
                    </p>
                    <div className="social-icons">
                        <a href="https://facebook.com" aria-label="Facebook"><FaFacebook /></a>
                        <a href="https://twitter.com" aria-label="Twitter"><FaTwitter /></a>
                        <a href="https://linkedin.com" aria-label="LinkedIn"><FaLinkedin /></a>
                        <a href="https://instagram.com" aria-label="Instagram"><FaInstagram /></a>
                    </div>
                </div>

                {/* Column 2: Quick Links */}
                <div className="footer-column">
                    <h3>{t('footer_links_title')}</h3>
                    <ul className="footer-links">
                        <li><a href="/">{t('home')}</a></li>
                        <li><a href="/UnderConstruction">{t('growth')}</a></li>
                        <li><a href="/UnderConstruction">{t('communication')}</a></li>
                        <li><a href="/Contact">{t('contact')}</a></li>
                    </ul>
                </div>

                {/* Column 3: Contact Info */}
                <div className="footer-column">
                    <h3>{t('footer_contact_title')}</h3>
                    <div className="contact-info">
                        <FaLocationDot className="contact-icon" />
                        <p>{t('footer_address')}</p>
                    </div>
                    <div className="contact-info">
                        <FaPhone className="contact-icon" />
                        <p>{t('footer_phone')}</p>
                    </div>
                    <div className="contact-info">
                        <FaEnvelope className="contact-icon" />
                        <p>{t('footer_email')}</p>
                    </div>
                </div>
            </div>

            <div className="footer-bottom">
                © {new Date().getFullYear()} {t('logo')} | {t('footer_all_rights')}
            </div>
        </footer>
    );
};

export default Footer;
