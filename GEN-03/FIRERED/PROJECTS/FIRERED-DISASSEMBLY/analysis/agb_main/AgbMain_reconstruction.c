/*
 * Logical reconstruction of FireRed AgbMain across the eight audited ROMs.
 *
 * This is a reconstruction artifact, not yet the final compiler-matched
 * src/main.c.  The final source will be promoted only after the surrounding
 * runtime, globals, compiler settings and linker layout are in place and every
 * target can be verified byte-for-byte.
 *
 * Regional differences verified from the ROMs are expressed with the explicit
 * FEATURE_* predicates supplied by config/targets.mk.  In particular, do not
 * replace FEATURE_FLASH_MEMORY_GUARD with a simple revision-number test.
 */

#include "build_features.h"

void AgbMain(void)
{
    RegisterRamReset(RESET_ALL);
    *(volatile unsigned short *)BG_PLTT = RGB_WHITE;

    InitGpuRegManager();
    REG_WAITCNT = WAITCNT_PREFETCH_ENABLE | WAITCNT_WS0_S_1 | WAITCNT_WS0_N_3;
    InitKeys();
    InitIntrHandlers();
    m4aSoundInit();
    EnableVCountIntrAtLine150();
    InitRFU();
    CheckForFlashMemory();
    InitMainCallbacks();
    InitMapMusic();
    ClearDma3Requests();
    ResetBgs();
    InitHeap(gHeap, HEAP_SIZE);
    SetDefaultFontsPointer();

    gSoftResetDisabled = FALSE;
    gHelpSystemEnabled = FALSE;
    SetNotInSaveFailedScreen();

#if FEATURE_PRINT_INIT
    AGBPrintInit();
#endif

#if FEATURE_FLASH_MEMORY_GUARD
    if (gFlashMemoryPresent != TRUE)
        SetMainCallback2(NULL);
#endif

    gLinkTransferringData = FALSE;

    for (;;)
    {
        ReadKeys();

        if (gSoftResetDisabled == FALSE
         && (gMain.heldKeysRaw & A_BUTTON)
         && (gMain.heldKeysRaw & (B_BUTTON | START_BUTTON | SELECT_BUTTON))
              == (B_BUTTON | START_BUTTON | SELECT_BUTTON))
        {
            rfu_REQ_stopMode();
            rfu_waitREQComplete();
            DoSoftReset();
        }

        if (Overworld_SendKeysToLinkIsRunning() == TRUE)
        {
            gLinkTransferringData = TRUE;
            UpdateLinkAndCallCallbacks();
            gLinkTransferringData = FALSE;
        }
        else
        {
            gLinkTransferringData = FALSE;
            UpdateLinkAndCallCallbacks();

            if (Overworld_RecvKeysFromLinkIsRunning() == 1)
            {
                gMain.newKeys = 0;
                ClearSpriteCopyRequests();
                gLinkTransferringData = TRUE;
                UpdateLinkAndCallCallbacks();
                gLinkTransferringData = FALSE;
            }
        }

        PlayTimeCounter_Update();
        MapMusicMain();
        WaitForVBlank();
    }
}
