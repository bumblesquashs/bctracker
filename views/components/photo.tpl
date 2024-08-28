
<style>
    .photo-container {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    
    .photo {
        width: 100%;
        aspect-ratio: 4 / 3;
    }
    
    .photo-container .credit {
        font-size: 11pt;
        color: #666666;
    }
    
    .photo .placeholder {
        background-color: #CBCBCB;
        text-align: center;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #2F2F2F;
        --image-size: 100px;
        --image-color: #2F2F2F;
    }
    
    .info-box .photo-container {
        margin-bottom: 10px;
    }
    
    .info-box .photo {
        width: calc(100% + 20px);
        margin: -10px -10px 0px -10px;
    }
</style>

<div class="photo-container">
    <div class="photo">
        % if photo:
            % pass
        % else:
            <div class="placeholder">
                <div class="column center">
                    % include('components/svg', name='photo')
                    Photo unavailable
                </div>
            </div>
        % end
    </div>
    % if photo:
        % if photo.url:
            <a class="credit" href="{{ photo.url }}">{{ photo.credit }}</a>
        % else:
            <div class="credit">{{ photo.credit }}</div>
        % end
    % end
</div>
