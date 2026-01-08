package com.aegisops.api.security;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class SecurityConfig implements Filter {

    private static final String API_KEY = "AegisOps-Secret-2026";

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest httpReq = (HttpServletRequest) request;
        String key = httpReq.getHeader("X-API-KEY");

        if (key == null || !key.equals(API_KEY)) {
            HttpServletResponse httpRes = (HttpServletResponse) response;
            httpRes.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            httpRes.getWriter().write("Unauthorized: Missing or invalid API Key");
            return;
        }

        chain.doFilter(request, response);
    }
}
